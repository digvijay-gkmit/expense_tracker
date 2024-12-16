from rest_framework import serializers
from .models import CustomUser
from category.models import Category 
PREDEFINED_CATEGORIES = [
    'Salary',
    'Food',
    'Transport',
    'Entertainment',
]

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating User instances.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)

        for category_name in PREDEFINED_CATEGORIES:
            category, created = Category.objects.get_or_create(name=category_name)
            user.categories.add(category)

        return user




