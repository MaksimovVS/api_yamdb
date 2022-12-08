# reviews/admin.py

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from reviews.models import Comment, Review, Category, Genre, Title


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        fields = (
            "id",
            "author",
            "title",
            "text",
            "score",
            "pub_date",
        )


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = (ReviewResource,)
    list_display = ("author", "title", "text", "score", "pub_date")
    search_fields = ("title",)
    list_filter = ("author", "title")
    empty_value_display = "-пусто-"


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "review",
            "text",
            "pub_date",
        )


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    resource_classes = (CommentResource,)
    list_display = ("author", "review", "text", "pub_date")
    search_fields = ("review",)
    list_filter = ("author", "review")
    empty_value_display = "-пусто-"


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = (CategoryResource,)
    list_display = ("name", "slug")
    search_fields = ("name",)
    list_filter = ("name", "slug")
    empty_value_display = "-пусто-"


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
            "slug",
        )


@admin.register(Genre)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = (GenreResource,)
    list_display = ("name", "slug")
    search_fields = ("name",)
    list_filter = ("name", "slug")
    empty_value_display = "-пусто-"


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "category",
            "genre",
            "description"
        )


@admin.register(Title)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = (TitleResource,)
    list_display = (
        "id",
        "name",
        "year",
        "category",
        "description"
    )
    search_fields = ("name",)
    list_filter = ("category",)
    empty_value_display = "-пусто-"
