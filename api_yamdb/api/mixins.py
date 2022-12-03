# api/mixins.py

from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)


class CreateListDestroyViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass
