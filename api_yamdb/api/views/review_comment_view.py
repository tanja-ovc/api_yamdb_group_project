from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from reviews.models import Title
from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import AdminAuthorModeratorOrReadOnly

PERMISSION_ERROR = 'Изменение чужого контента запрещено!'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminAuthorModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(PERMISSION_ERROR)
        super(ReviewViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminAuthorModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        return review.comments.all()
