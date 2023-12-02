from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (request.user.is_staff or request.user.is_superuser)


class IsOddiyAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.oddiy_admin)


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
