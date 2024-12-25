from django.db import models
from user.models import CustomUser
import uuid
from base.models import BaseModel

# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="categories",
    )
    is_active = models.BooleanField(default=True)  # False => Soft-deleted
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
