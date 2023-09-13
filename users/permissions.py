from rest_framework import permissions

class IsNotStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is not staff (i.e., is_staff is False)
        return not request.user.is_staff
