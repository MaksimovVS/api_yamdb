from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Genre, Category
from .filters import TitleFilter
from .permissions import (ReviewAndCommentsPermission, GenreCategoryPermission,
                          TitlePermission)
from .serializers import (TitleListSerializer, TitleSerializer,
                          GenreSerializer, CommentSerializer,
                          CategorySerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обзоров"""
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = [ReviewAndCommentsPermission, ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = [ReviewAndCommentsPermission, ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        return review.comments.all()
