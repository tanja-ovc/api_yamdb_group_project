from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('users', views.MyUserViewSet, basename='users')
router.register('titles', views.TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.send_confirmation_code),
]
