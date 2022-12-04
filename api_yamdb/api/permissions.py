# api/permissions.py

from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    pass


class ReviewAndCommentsPermission(permissions.BasePermission):
    pass
