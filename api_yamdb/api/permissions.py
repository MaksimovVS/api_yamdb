# api/permissions.py

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class ReviewAndCommentsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (obj.author == request.user
                     or request.user.is_admin
                     or request.user.is_moderator)
                )
