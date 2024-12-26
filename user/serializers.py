from rest_framework import serializers
from .models import CustomUser
from category.models import Category
import re
from django.utils.crypto import get_random_string

from rest_framework.response import Response


def validate_password_base(value):
    """
    Validator for passwords.

    Args:
        password: The password string to validate.

    Raises:
        serializers.ValidationError: With a clear message about the missing requirement.
    """

    MIN_LENGTH = 8
    requirements = (
        ("uppercase letter", r"[A-Z]"),
        ("lowercase letter", r"[a-z]"),
        ("number", r"\d"),
        ("special character", r"[!@#$%^&*()_+{}\[\]:;<>,.?~-]"),
    )

    if len(value) < MIN_LENGTH:
        raise serializers.ValidationError(
            "value must be at least {} characters long.".format(MIN_LENGTH)
        )

    missing_requirements = []
    for name, pattern in requirements:
        if not re.search(pattern, value):
            missing_requirements.append(name)

    if missing_requirements:
        message = "Password must contain at least one of the following: " + ", ".join(
            missing_requirements
        )
        raise serializers.ValidationError(message)

    return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating User instances.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "is_verified",
            "is_active",
            "is_admin",
        ]

    def validate_username(self, value):
        """
        Validates the username:
            - Must be all lowercase.
            - Only periods and underscores are allowed as special characters.
            - Must not already exist in the database.
        """
        if not all(c.isalnum() or c in [".", "_"] for c in value):
            raise serializers.ValidationError(
                "Username can only contain alphanumeric characters, periods (.), and underscores (_)."
            )

        if not value.islower():
            raise serializers.ValidationError("Username must be all lowercase.")

        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value

    def validate_password(self, value):
        """password validation"""

        return validate_password_base(value)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data.pop("password")

        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):

        validate_password_base(value)
        return value

    def validate(self, data):
        # Check if new password and confirm password match
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "New passwords must match."}
            )
        return data
