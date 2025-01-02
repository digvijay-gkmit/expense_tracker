from base.permissions import IsAdminOrOwner 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Category
from .serializers import CategorySerializer
from django.shortcuts import get_object_or_404
from base.pagination import CustomPagination


class CategoryView(APIView):
    """
    Handle all operations (list, create, retrieve, update, delete) for categories.
    """
    permission_classes = [IsAdminOrOwner]  # Add only the custom permission

    def get(self, request, pk=None):
        """
        Handle both listing all categories (if no pk) and retrieving a single category (if pk provided).
        """
        user = request.user
        if pk is None:
            # List all categories
            if user.is_admin:
                categories = Category.objects.filter(is_active=True)
            else:
                categories = Category.objects.filter(
                    Q(user_id=user) | Q(user_id=None), is_active=True
                )
            serializer = CategorySerializer(categories, many=True)
            page_number = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 5)
            return Response(serializer.data)
        else:
            # Retrieve a specific category
            category = get_object_or_404(Category, id=pk)
            self.check_object_permissions(request, category)  # Check object-level permission
            serializer = CategorySerializer(category)
            return Response(serializer.data)


class CategoryView(APIView):
    """
    Handle all operations (list, create, retrieve, update, delete) for categories.
    """
    permission_classes = [IsAdminOrOwner]
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        """
        Handle both listing all categories (if no pk) and retrieving a single category (if pk provided).
        """
        user = request.user
        
        if pk is None:
            # List all categories
            if user.is_admin:
                queryset = Category.objects.filter(is_active=True)
            else:
                queryset = Category.objects.filter(
                    Q(user_id=user) | Q(user_id=None), 
                    is_active=True
                )

            # Initialize paginator
            paginator = self.pagination_class()
            
            # Paginate the queryset
            paginated_queryset, total_count = paginator.paginate_queryset(
                queryset=queryset,
                request=request
            )
            
            # Serialize the paginated data
            serializer = CategorySerializer(paginated_queryset, many=True)
            
            # Return paginated response
            return paginator.get_paginated_response(
                data=serializer.data,
                request=request,
                total_count=total_count
            )
        else:
            # Retrieve a specific category
            category = get_object_or_404(Category, id=pk)
            self.check_object_permissions(request, category)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new category.
        """
        data = request.data
        user = request.user
        if user.is_admin:
            if 'user' not in data:
                data['user'] = None
        else:
            data['user'] = user.id

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Update a category.
        """
        category = get_object_or_404(Category, id=pk)
        self.check_object_permissions(request, category)  # Check object-level permission
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        """
        Partially update a category.
        """
        category = get_object_or_404(Category, id=pk)
        self.check_object_permissions(request, category)  # Check object-level permission
        if 'is_active' in request.data and not request.user.is_admin:
            return Response(
                {"error": "You do not have permission to deactivate this category."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Delete a category.
        """
        category = get_object_or_404(Category, id=pk)
        self.check_object_permissions(request, category)  # Check object-level permission
        category.is_active = False
        category.save()
        return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)