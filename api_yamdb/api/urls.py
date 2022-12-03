from django.urls import path, include

from api.views import SignUpSet, TokenSet

urlpatterns = [
    path('v1/auth/signup/', SignUpSet.as_view(), name='signup'),
    path('v1/auth/token/', TokenSet.as_view(), name='token'),
]
