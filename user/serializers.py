from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating User instances.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user




