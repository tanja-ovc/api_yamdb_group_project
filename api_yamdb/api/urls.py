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
router.register('users', views.MyUserViewSet)

urlpatterns = [
    path('v1/categories/', views.CategoryList.as_view(),
         name='categories'),
    path('v1/categories/<slug:slug>/', views.CategoryDetail.as_view(),
         name='category'),
    path('v1/genres/', views.GenreList.as_view(),
         name='genres'),
    path('v1/genres/<slug:slug>/', views.GenreDetail.as_view(),
         name='genre'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.send_confirmation_code),
    path('v1/auth/token/', views.compare_confirmation_code),
]
