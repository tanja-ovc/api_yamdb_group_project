from rest_framework import filters
from rest_framework import serializers

from api.permissions import AdminOrReadOnly
from reviews.models import Category


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category_name',)

    class Meta:
        fields = ('id', 'category_name', 'slug')
        model = Category
