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
            data={
                    "message": "User created successfully.",
                    "access_token": str(refresh.access_token),  # JWT access token
                    "refresh_token": str(refresh),  # JWT refresh token
                }
            return Response(
                data,
                content_type="application/json",
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
        
        if user is not None:
            # Issue JWT Token for the authenticated user
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


# class UserTestView(APIView):
#     """
#     Test view to check if the user is authenticated.
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         # Accessing the authenticated user
#         user = request.user
#         print(user) 
#         # Returning a personalized message
#         return Response({"message": f"You are an authenticated user, {user.username}."})
    



class UserLogoutView(APIView):
    """
    User Logout View to revoke the refresh token and log the user out.
    """

    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        
        try:
            refresh_token = request.data.get("refresh_token")
            access_token= request.data.get("access_token")
            # print(refresh_token)
            if refresh_token:
                refresh = RefreshToken(refresh_token)
                accesss= AccessToken(access_token)
                refresh.blacklist()  # Blacklist the token
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



class UserUpdateView(APIView):
    """
    User Update View to allow authenticated users to update their profile information.
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        """
        Handle PUT request to update user information.
        Allows updating name, mobile number, and password.
        """
        user = request.user
        
        # Extract update data
        name = request.data.get('name')
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')
        
        # Prepare update data
        update_data = {}
        
        # Add name if provided
        if name:
            update_data['name'] = name
        
        # Add mobile number if provided
        if mobile_number:
            update_data['mobile_number'] = mobile_number
        
        # Handle password update with additional security
        if password:
            # You might want to add additional password validation here
            update_data['password'] = make_password(password)
        
        # If no update data is provided
        if not update_data:
            return Response(
                {"message": "No update information provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create serializer with partial update
        serializer = UserSerializer(user, data=update_data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User profile updated successfully."},
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )


class UserDeleteView(APIView):
    """
    User Delete View to allow authenticated users to delete their account.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """
        Handle DELETE request to remove the user's account.
        Requires the user to be authenticated.
        """
        user = request.user
        
        try:
            # Delete the user
            user.delete()
            return Response(
                {"message": "User account deleted successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "Error deleting user account.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )