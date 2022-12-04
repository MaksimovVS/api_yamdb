# api/serializers.py

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ("email", "username")


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    @staticmethod
    def get_token(user):
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
        }

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        # read_only_fields = ('role',)


class MeSerializer(serializers.ModelSerializer):

     class Meta:
         model = User
         fields = ('username', 'email', 'first_name', 'last_name', 'bio',)


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Category
        exclude = ["id"]


class GenreSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Genre
        exclude = ["id"]


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
            "id",
            "name",
            "year",
            "genre",
            "category",
            "description",
            "rating",
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
        slug_field="username", read_only=True,
    )

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    {"message": "Вы уже оставили отзыв на это произведение."}
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username", read_only=True,
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ["review"]
