from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from base.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            # verification_token=get_random_string(64),  # Generate verification token
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_verified", True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, BaseModel):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    mobile_no = models.CharField(max_length=13, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(
        default=False
    )  # added for email verification and permissions
    is_active = models.BooleanField(default=True)
    # verification_token = models.CharField(
    #     max_length=64, unique=True, null=True, blank=True
    # )
    # token_created_at = models.DateTimeField(null=True, blank=True)  # Add this field

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email

    def is_staff(self):
        """If the user is an admin, they are considered 'staff'."""
        return self.is_admin

    # def generate_new_verification_token(self):
    #     """Generate a new verification token for the user."""

    #     self.verification_token = get_random_string(64)
    #     self.token_created_at = timezone.now()  # Set token creation time
    #     self.save()
    #     return self.verification_token

    # def is_verification_token_valid(self):
    #     """Check if the verification token is still valid (not expired)."""

    #     if not self.token_created_at:
    #         return False

    #     # Token expires after 24 hours
    #     expiry_time = self.token_created_at + timedelta(hours=24)
    #     return timezone.now() <= expiry_time

    # def verify_email(self):
    #     """Mark the user's email as verified and clear the verification token."""
    #     if self.is_verification_token_valid():
    #         self.is_verified = True
    #         self.verification_token = None
    #         self.token_created_at = None
    #         self.save()
    #         return True
    #     return False


# class IsEmailVerifiedPermission(BasePermission):
#     """
#     Permission check for email verification.
#     """

#     message = (
#         "Email verification required. Please verify your email to access this resource."
#     )

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.email_verified()
