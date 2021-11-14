from rest_framework import filters
from rest_framework import serializers

from api.permissions import AdminOrReadOnly
from reviews.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='name')

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('genre_name',)

    class Meta:
        fields = ('id', 'genre_name', 'slug')
        model = Genre
