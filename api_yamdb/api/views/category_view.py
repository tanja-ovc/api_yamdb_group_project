from rest_framework import filters, viewsets, mixins

from api.permissions import AdminOrReadOnly
from api.serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering = ('name',)