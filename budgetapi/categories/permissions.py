from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAuthenticatedAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        # TODO POST handler
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.user == request.user:
            return True

        raise PermissionDenied(
            {"message": f"You don't have permission to access object id {obj.id}."}
        )