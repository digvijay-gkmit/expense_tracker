from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from .models import Category
from .serializers import CategorySerializer


# Helper function to get category
def get_category(pk):
    try:
        return Category.objects.get(id=pk)
    except Category.DoesNotExist:
        raise NotFound({"error": "Category not found"})

    
class CategoryListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_admin:
            # Admins can see all active categories, regardless of the user_id
            categories = Category.objects.filter(is_active=True)
        else:
            # Normal users can only see their own categories or global categories
            categories = Category.objects.filter(
                Q(user_id=user) | Q(user_id=None), is_active=True
            )
        
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user

        # Admins can set any user_id for a category
        if user.is_admin:
            if 'user' in data:
                pass
            else:
                data['user'] = None
        else:
            # Normal users can only create categories for themselves
            data['user'] = user.id
        
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryRetrieveUpdateDestroyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        category = get_category(pk)
        # Admins can retrieve any category, normal users can only retrieve their own or global categories
        if request.user.is_admin:
            pass
        elif category.user_id != request.user.id and category.user_id is not None:
            return Response({"error": "You can only view your own categories."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk=None):
        category = get_category(pk)
        if request.user.is_admin:
            pass  # Admins can update any category
        elif category.user_id != request.user.id:
            return Response({"error": "You can only update your own categories."}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):

        category = get_category(pk)
        if request.user.is_admin:
            pass  # Admins can update any category
        elif category.user_id != request.user.id:
            return Response({"error": "You can only update your own categories."}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        category = get_category(pk)
        # Admins can soft delete any category, normal users can only soft delete their own categories
        if request.user.is_admin:
            category.is_active = False  # False = soft deleted
            category.save()
            return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)
        elif category.user_id == request.user.id:
            category.is_active = False  # False = soft deleted
            category.save()
            return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You can only delete your own categories."}, status=status.HTTP_403_FORBIDDEN)
