# api/permissions.py

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


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

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return False


class ReviewAndCommentsPermission(permissions.BasePermission):

    ROLE = ("admin", "moderator")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj.author == request.user
                    or request.user.role in self.ROLE)
        return request.method in permissions.SAFE_METHODS
