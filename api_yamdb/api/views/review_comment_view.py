from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from reviews.models import Title
from api.serializers import ReviewSerializer, CommentSerializer

PERMISSION_ERROR = 'Изменение чужого контента запрещено!'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role not in ('admin', 'moderator') and instance.author != user:
            raise PermissionDenied(PERMISSION_ERROR)
        super(ReviewViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        user = self.request.user
        author = serializer.instance.author
        if user.role not in ('admin', 'moderator') or author != user:
            raise PermissionDenied(PERMISSION_ERROR)
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role not in ('admin', 'moderator') and instance.author != user:
            raise PermissionDenied(PERMISSION_ERROR)
        super(CommentViewSet, self).perform_destroy(instance)
