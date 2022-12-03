# api/permissions.py

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    pass


class ReviewAndCommentsPermission(permissions.BasePermission):
    pass
