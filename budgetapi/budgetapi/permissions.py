from rest_framework import permissions

class IsAuthenticatedAdminOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or (obj.user == request.user):
            return True
        raise PermissionDenied(
            {"message": "You don't have permission to access {obj.id}."}
        )