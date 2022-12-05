# api/mixins.py

from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)


class CreateReadDestroyViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass
