from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """Check if user is a superuser
        """
        return request.user.is_superuser