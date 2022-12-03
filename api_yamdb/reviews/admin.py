# reviews/admin.py

from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отображаем текст обзора, автора,
    оценку и дату"""
    list_display = (
        'author',
        'title',
        'text',
        'score',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('author', 'title')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отображаем текст комментария, автора,
    обзор к которому относится и дату"""
    list_display = (
        'author',
        'review',
        'text',
        'pub_date'
    )
    search_fields = ('review',)
    list_filter = ('author', 'review')
    empty_value_display = '-пусто-'
