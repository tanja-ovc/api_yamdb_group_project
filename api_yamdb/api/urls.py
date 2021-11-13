from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('users', views.MyUserViewSet)

urlpatterns = [
    path('v1/auth/signup/', views.send_confirmation_code),
    path('v1/auth/token/', views.compare_confirmation_code),
    path('v1/users/me/', views.UserAPI.as_view()),
    path('v1/', include(router.urls)),
]
