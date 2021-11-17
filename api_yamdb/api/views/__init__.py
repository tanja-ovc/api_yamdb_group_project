from .auth_user_view import (MyUserViewSet,
                             send_confirmation_code,
                             compare_confirmation_code,
                             UserAPI,)
from .review_comment_view import ReviewViewSet, CommentViewSet
from .title_view import TitleViewSet
from .category_view import CategoryViewSet
from .genre_view import GenreViewSet

__all__ = [
    'MyUserViewSet',
    'send_confirmation_code',
    'compare_confirmation_code',
    'UserAPI',
    'ReviewViewSet',
    'CommentViewSet',
    'TitleViewSet',
    'CategoryViewSet',
    'GenreViewSet',
]
