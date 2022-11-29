from django.urls import path, include
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register(r'auth/signup/', SignUpSet)

urlpatterns = [
    path('v1/', include(router_v1.usrl))
]
