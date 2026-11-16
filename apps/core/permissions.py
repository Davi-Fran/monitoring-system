from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.core.utils import is_admin

class IsAdminOrReadOnly(BasePermission):
    message = "Only superusers and staffs can change the data"

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return is_admin(user)


class IsAdminOrSelf(BasePermission):
    message = "You can only edit your own data."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return is_admin(request.user) or obj == request.user


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)