from rest_framework import filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly
from api.serializers.title_serializer import TitleSerializer
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_class = TitleFilter
    ordering = ('id',)
