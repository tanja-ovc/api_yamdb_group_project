from rest_framework import filters
from rest_framework import serializers

from .genre_title_serializer import Genre_TitleSerializer
from api.permissions import AdminOrReadOnly
from reviews.models import Category, Genre, Genre_Title, Title


class TitleSerializer(serializers.ModelSerializer):
    title_name = serializers.CharField(source='name')
    year = serializers.IntegerField()
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genres = Genre_TitleSerializer(many=True)
    reviews = serializers.StringRelatedField(read_only=True, many=True)

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title_name', 'year', 'category__slug', 'genres__genre__slug')

    class Meta:
        fields = ('id', 'title_name', 'year', 'description',
                  'category', 'genres', 'reviews')
        model = Title
        read_only_fields = ('author', 'reviews',)

    # def validate_genres(self, value):
    #     # request = self.context['request']
    #     value = ''
    #     if isinstance(value, str) is False:
    #         raise serializers.ValidationError(
    #             'Поле "genres" должно содеражть строку/список строк.'
    #         )
    #     return value


class TitleSerializerWrite(serializers.ModelSerializer):
    title_name = serializers.CharField(source='name')
    year = serializers.IntegerField()
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genres = serializers.SlugRelatedField(
        slug_field='genre', queryset=Genre_Title.objects.all()
    )
    reviews = serializers.StringRelatedField(read_only=True, many=True)

    permission_classes = (AdminOrReadOnly,)

    class Meta:
        fields = ('id', 'title_name', 'year', 'description',
                  'category', 'genres', 'reviews')
        model = Title
        read_only_fields = ('author', 'reviews',)
