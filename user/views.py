from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer 
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError



class UserSignupView(APIView):
    """
    User Signup View to create a new user and issue a JWT.
    """

    permission_classes = [permissions.AllowAny]  # Anyone can access the signup view

    def post(self, request):
        """
        Handle POST request to sign up a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Issue JWT Token for the new user
            refresh = RefreshToken.for_user(user)
            print(refresh)
            return Response(
                {
                    "message": "User created successfully.",
                    "access_token": str(refresh.access_token),  # JWT access token
                    "refresh_token": str(refresh),  # JWT refresh token
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        # print(user)
        if user is not None:
            # Issue JWT Token for the authenticated user
            refresh = RefreshToken.for_user(user)
            
            data = {
                "message": "Login successful.",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
            return Response(
                # {
                #     "message": "Login successful.",
                #     "access_token": str(refresh.access_token),
                #     "refresh_token": str(refresh),
                # },
                data,
                content_type="application/json",
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


# class UserLogoutView(APIView):
#     """
#     User Logout View to revoke the refresh token and log the user out.
#     """

#     permission_classes = [
#         permissions.IsAuthenticated
#     ]  # Only authenticated users can log out

#     def post(self, request):
#         """
#         Handle POST request to logout a user by blacklisting the refresh token.
#         """
#         try:
#             # Get the refresh token from the request
#             refresh_token = request.data.get("refresh_token")
#             print(refresh_token)
#             # print(refresh_token)
#             if refresh_token:
#                 # Try to decode the token and blacklist it
#                 refresh = RefreshToken(refresh_token)
#                 # Blacklist the refresh token
#                 refresh.blacklist()

#                 return Response(
#                     {"message": "Logout successful."},
#                     status=status.HTTP_200_OK,
#                 )
#             else:
#                 return Response(
#                     {"message": "Refresh token is required."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except TokenError:
#             return Response(
#                 {"message": "Invalid refresh token."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


class UserTestView(APIView):
    """
    Test view to check if the user is authenticated.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Accessing the authenticated user
        user = request.user
        print(user) 
        # Returning a personalized message
        return Response({"message": f"You are an authenticated user, {user.username}."})
    



class UserLogoutView(APIView):
    """
    User Logout View to revoke the refresh token and log the user out.
    """

    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        print("im inside logout view")
        try:
            refresh_token = request.data.get("refresh_token")
            access_token= request.data.get("access_token")
            print(refresh_token)
            if refresh_token:
                refresh = RefreshToken(refresh_token)
                accesss= AccessToken(access_token)
                refresh.blacklist()  # Blacklist the token
                accesss.blacklist()
                return Response({
                    "message": "Logout successful."
                }, status=status.HTTP_200_OK)

            return Response({
                "message": "Refresh token is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({
                "message": "Invalid refresh token."
            }, status=status.HTTP_400_BAD_REQUEST)

