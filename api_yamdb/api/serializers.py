# api/serializers.py

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.validators import UsernameValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            UsernameValidator(),
            UnicodeUsernameValidator()
        )
    )
    email = serializers.EmailField(validators=(UnicodeUsernameValidator(),))


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=(
            UsernameValidator(),
            UnicodeUsernameValidator()
        )
    )

    class Meta:
        model = User
        fields = (
            "username",
            "confirmation_code",
        )


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            UsernameValidator(),
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=User.objects.all()),
        )
    )
    email = serializers.EmailField(
        validators=(
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=User.objects.all()),
        )
    )

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role",
        )


class NotChangeRoleSerializer(UsersSerializer):
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre
        lookup_field = "slug"


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id", "name", "year", "genre", "category", "description", "rating",
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(title=title_id, author=author).exists():
            raise serializers.ValidationError(
                {"message": "Вы уже оставили отзыв на это произведение."}
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ["review"]
