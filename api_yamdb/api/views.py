# api/views.py

from django.db.models import Avg
from rest_framework import filters, viewsets, status
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import SignUpSerializer, TokenSerializer
from users.models import User
from api.permissions import IsAdminOrReadOnly
from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleReadSerializer, TitleWriteSerializer,)
from api.pagination import PageNumberPagination
from reviews.models import Category, Genre, Title


class SignUpSet(CreateAPIView):

    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Регистрация на YaMDb',
            f'Здравствуйте, {user.username}! Вы зарегистрировались на YaMDb.ru.\n'
            f'confirmation_code для получения токена:\n{confirmation_code}',
            'registrate@YaMDb.ru',
            (user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenSet(CreateAPIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.get(username=data['username'])
        token = data['confirmation_code']
        if default_token_generator.check_token(user, token):
            token = RefreshToken.for_user(user).access_token
            return Response({'JWT': str(token)},  status=status.HTTP_200_OK)
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")
    ).order_by(
        "id"
    )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TitleWriteSerializer
        return TitleReadSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
