from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer, ChangePasswordSerializer
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.hashers import make_password
from django.db import transaction
from base.permissions import IsAdminOrUserOwner
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.crypto import get_random_string


class UserSignupView(APIView):
    """
    User Signup View to create a new user and issue a JWT.
    """

    permission_classes = [permissions.AllowAny]  # Anyone can access the signup view

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            try:
                # serializer.validated_data["verification_token"] = get_random_string(64)
                user = serializer.save()
                # Get your domain from settings or use request
                domain = request.get_host()

                # Generate verification URL with actual domain
                verification_url = (
                    f"http://{domain}/user/verify-email/{user.generate_new_verification_token()}/"
                )

                # Prepare email content
                email_subject = "Verify your email address"
                email_body = render_to_string(
                    "email/verify_email.html",
                    {
                        "user": user,
                        "verification_url": verification_url,
                        "domain": domain,
                    },
                )

                # Create and send email
                email = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)

                return Response(
                    {
                        "message": "User created successfully. Please check your email for verification.",
                        "email": user.email,
                    },
                    status=status.HTTP_201_CREATED,
                )

            except Exception as e:
                print(f"Email sending failed: {str(e)}")
                # You might want to delete the user if email sending fails
                return Response(
                    {
                        "message": "User created but email sending failed. Please try again.",
                        "error": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            user = CustomUser.objects.get(verification_token=token)
            if not user.is_verified:
                user.is_verified = True
                user.verification_token = None  # Clear token after use
                user.save()
                return Response(
                    {"message": "Email verified successfully. You can now login."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Email already verified."}, status=status.HTTP_200_OK
            )

        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Invalid verification token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginView(APIView):
    """
    User Login View to authenticate a user and return JWT.
    """

    permission_classes = [permissions.AllowAny]  # Anyone can access the login view

    def post(self, request):
        """
        Handle POST request to authenticate the user and return a JWT.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Issue JWT Token for the authenticated user
            if not user.is_active:
                return Response(
                    {"message": "User account is disabled."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            refresh = RefreshToken.for_user(user)

            data = {
                "message": "Login successful.",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
            return Response(
                data,
                content_type="application/json",
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserLogoutView(APIView):
    """
    User Logout View to revoke the refresh token and log the user out.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data.get("refresh_token")
            
            # print(refresh_token)
            if refresh_token:
                refresh = RefreshToken(refresh_token)

                refresh.blacklist()  # Blacklist the token
                return Response(
                    {"message": "Logout successful."}, status=status.HTTP_200_OK
                )

            return Response(
                {"message": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except TokenError:
            return Response(
                {"message": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetailView(APIView):
    """
    API endpoint for retrieving, updating, and deleting user details.
    """

    permission_classes = [IsAdminOrUserOwner]

    def get(self, request, pk=None):
        """
        Retrieve user details.
        """
        
        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
        else:
            user = request.user

        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        if request.user.is_admin:
            return Response(serializer.data)
        
        data={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
        }    
        return Response(data)

    def put(self, request, pk=None):
        """
        Update user details.
        """

        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
        else:
            user = request.user

        self.check_object_permissions(request, user)
        if request.data.get("password"):
            return Response(
                {"message": "Password cannot be updated using this endpoint"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data.get("email"):
            return Response(
                {"message": "Email cannot be updated using this endpoint"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        """
        Partially update user details.
        """
        if request.data.get("password"):
            return Response(
                {"message": "Password cannot be updated using this endpoint"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data.get("email"):
            return Response(
                {"message": "Email cannot be updated using this endpoint"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
        else:
            user = request.user

        self.check_object_permissions(request, user)

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Delete user account. #soft delete
        """

        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
        else:
            user = request.user

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data={"is_active":False}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "user deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    API endpoint for changing user password with JWT authentication.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        try:
            with transaction.atomic():
                user = CustomUser.objects.select_for_update().get(id=request.user.id)

                serializer = self.serializer_class(
                    data=request.data, context={"request": request}
                )

                if serializer.is_valid():
                    # Verify old password
                    if not user.check_password(
                        serializer.validated_data["old_password"]
                    ):
                        return Response(
                            {"old_password": "Current password is incorrect."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # Verify new password is different from old password
                    if (
                        serializer.validated_data["old_password"]
                        == serializer.validated_data["new_password"]
                    ):
                        return Response(
                            {
                                "new_password": "New password must be different from current password."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # Set new password
                    user.set_password(serializer.validated_data["new_password"])
                    user.save(update_fields=["password"])

                    # Generate new tokens
                    refresh = RefreshToken.for_user(user)

                    return Response(
                        {
                            "status": "success",
                            "message": "Password successfully changed.",
                            "access_token": str(refresh.access_token),
                            "refresh_token": str(refresh),
                        },
                        content_type="application/json",
                        status=status.HTTP_200_OK,
                    )

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error": "An error occurred while changing password.",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Password successfully changed."}, status=status.HTTP_200_OK
        )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


