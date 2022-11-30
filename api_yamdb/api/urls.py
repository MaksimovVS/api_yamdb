# api/urls.py

from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "api"

router_v1 = routers.DefaultRouter()


router_v1.register(
    "titles", views.TitlesViewSet, basename="title"
)
router_v1.register(
    "genres", views.GenreViewSet, basename="genre"
)
router_v1.register(
    "categories", views.CategoryViewSet, basename="category"
)


urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
