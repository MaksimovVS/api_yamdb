# api/views.py
from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.permissions import AllowAny

from api.serializers import SignUpSerializer
from users.models import User


class SignUpSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
