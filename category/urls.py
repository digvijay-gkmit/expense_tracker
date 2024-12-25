from django.urls import path
from .views import CategoryView

# URL patterns for CategoryViewSet actions
urlpatterns = [
    path('', CategoryView.as_view(), name='category-list-create'),
    path('<uuid:pk>/', CategoryView.as_view(), name='category-list-create'),
]
