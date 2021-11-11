from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import MyUserViewSet, send_confirmation_code

router = DefaultRouter()
router.register('users', MyUserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', send_confirmation_code),
]
