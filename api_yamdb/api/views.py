# api/views.py

from django.db.utils import IntegrityError
from django.db.models import Avg
from rest_framework import filters, viewsets, status
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from api_yamdb.settings import EMAIL
from users.models import User
from api.permissions import (
    ReviewAndCommentsPermission,
    IsAdminOrReadOnly,
    IsAdminOnly,
)
from api.filters import TitleFilter
from api.serializers import (
    SignUpSerializer,
    TokenSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    GenreSerializer,
    CommentSerializer,
    CategorySerializer,
    ReviewSerializer,
    UsersSerializer,
    NotChangeRoleSerializer,
)
from reviews.models import Category, Genre, Title


class SignUpSet(CreateAPIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            return Response(
                {"error": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            "Регистрация на YaMDb",
            f"Здравствуйте, {user.username}!"
            f"confirmation_code для получения токена:\n{confirmation_code}",
            EMAIL,
            (user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenSet(CreateAPIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data["username"])
        confirmation_code = data["confirmation_code"]
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user).access_token
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    permission_classes = (IsAdminOnly,)
    lookup_field = "username"

    @action(
        methods=("GET", "PATCH"),
        detail=False, permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == "GET":
            return Response(serializer.data)
        if request.user.is_admin:
            serializer = UsersSerializer(
                request.user, data=request.data, partial=True
            )
        else:
            serializer = NotChangeRoleSerializer(
                request.user, data=request.data, partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")).order_by("id")
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TitleWriteSerializer
        return TitleReadSerializer


class CategoryViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):

    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = ReviewSerializer
    permission_classes = [
        ReviewAndCommentsPermission,
    ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):

    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = CommentSerializer
    permission_classes = [
        ReviewAndCommentsPermission,
    ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = title.reviews.get(pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = title.reviews.get(pk=self.kwargs.get("review_id"))
        return review.comments.all()
