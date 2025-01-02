from rest_framework import serializers
from users.models import CustomUser
from .models import Category
from django.utils.text import slugify
from django.core.exceptions import ValidationError

def is_slug_unique(user, slug):
    if user is None:
        if Category.objects.filter(slug=slug, user=None).exists():
            raise ValidationError(
                f"A global category with the slug '{slug}' already exists."
            )
    else:
        if Category.objects.filter(slug=slug, user=user).exists():
            raise ValidationError(
                f"A category with the slug '{slug}' already exists under your account."
            )


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ['id','created_at', 'updated_at']

    def create(self, validated_data):
        """Override to generate the slug."""
        name = validated_data.get("name")
        slug = slugify(name)
        user = validated_data.get("user", None)
        try:
            is_slug_unique(user=user, slug=slug)
        except ValidationError as e:
            raise serializers.ValidationError({"slug": [str(e)]})
        validated_data["slug"] = slug

        # Create the category with the generated slug
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        """Override to generate the slug."""
        name = validated_data.get("name", instance.name)
        slug = slugify(name)
        user = validated_data.get("user", instance.user)

        if slug != instance.slug:
            try:
                is_slug_unique(user=user, slug=slug)
            except ValidationError as e:
                raise serializers.ValidationError({"slug": [str(e)]})
            is_slug_unique(user=user, slug=slug)
        # is_slug_unique(user=user, slug=slug)

        instance.slug = slug
        return super().update(instance, validated_data)        