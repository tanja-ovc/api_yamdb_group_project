from .auth_user_view import (MyUserViewSet,
                             send_confirmation_code,
<<<<<<< HEAD
                             compare_confirmation_code,
                             UserAPI,)
from .review_comment_view import ReviewViewSet, CommentViewSet
=======
                             compare_confirmation_code)
from .review_comment_view import ReviewViewSet, CommentViewSet
from .title_view import TitleViewSet
from .category_view import CategoryList, CategoryDetail
from .genre_view import GenreList, GenreDetail
>>>>>>> many-to-many/test

__all__ = [
    'MyUserViewSet',
    'send_confirmation_code',
    'compare_confirmation_code',
<<<<<<< HEAD
    'UserAPI',
    'ReviewViewSet',
    'CommentViewSet',
=======
    'ReviewViewSet',
    'CommentViewSet',
    'TitleViewSet',
    'CategoryList',
    'CategoryDetail',
    'GenreList',
    'GenreDetail',
>>>>>>> many-to-many/test
]
