from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Allows access only to the owner of an object or admin users.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_staff
