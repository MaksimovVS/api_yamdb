# api/permissions.py

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    pass


class ReviewAndCommentsPermission(permissions.BasePermission):
    pass


class GenreCategoryPermission(permissions.BasePermission):
    pass


class TitlePermission(permissions.BasePermission):
    pass
