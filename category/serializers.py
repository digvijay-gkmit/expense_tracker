from rest_framework import serializers
from user.models import CustomUser
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Category
        fields = "__all__"