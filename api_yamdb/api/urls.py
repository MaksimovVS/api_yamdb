from django.urls import path, include

from api.views import SignUpSet

urlpatterns = [
    path('v1/auth/signup/', SignUpSet.as_view(), name='signup')
]
