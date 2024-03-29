# api/urls.py

from django.urls import include, path
from rest_framework import routers

from api.views import (
    SignUpSet,
    TokenSet,
    TitlesViewSet,
    GenreViewSet,
    CategoryViewSet,
    CommentViewSet,
    ReviewViewSet,
    UsersViewSet,
)

app_name = "api"

router_v1 = routers.DefaultRouter()


router_v1.register("titles", TitlesViewSet, basename="title")
router_v1.register("genres", GenreViewSet, basename="genre")
router_v1.register("categories", CategoryViewSet, basename="category")
router_v1.register(
    "titles/(?P<title_id>\\d+)/reviews",
    ReviewViewSet, basename="reviews",
)
router_v1.register(
    "titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments",
    CommentViewSet, basename="comments",
)
router_v1.register("users", UsersViewSet, basename="users")

auth_patterns = [
    path("signup/", SignUpSet.as_view(), name="signup"),
    path("token/", TokenSet.as_view(), name="token"),
]

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/", include(auth_patterns)),
]
