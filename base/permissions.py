from rest_framework.permissions import BasePermission


class IsAdminOrUserOwner(BasePermission):
    """
    Custom permission to only allow the owner or an admin to access or modify a user profile.
    """

    def has_permission(self, request, view):
        """
        This method checks if the user has permission at the view level.
        """
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        This method checks if the user has permission to access or modify the specific user object.
        """
        if request.user == obj:
            return True

        if request.user.is_admin:
            return True
        return False


class IsAdminOrOwner(BasePermission):
    """
    Custom permission to only allow admins or the owner of an object to access it.
    """

    def has_permission(self, request, view):
        """
        This method checks if the user has permission at the view level.
        """
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        This method checks if the user has permission at the object level.
        """
        if hasattr(obj, "user") and obj.user == request.user:
            return True

        if request.user.is_admin:
            return True

        return False