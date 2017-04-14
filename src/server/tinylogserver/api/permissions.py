"""TinyLog API Permission Classes"""

from rest_framework import permissions

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """Object-level permission for resources that belong to a specific user"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.is_staff
        else:
            return False
