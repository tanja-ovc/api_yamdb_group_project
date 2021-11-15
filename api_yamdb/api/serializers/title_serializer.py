from rest_framework import serializers

from .category_serializer import CategorySerializer
from .genre_serializer import GenreSerializer
from reviews.models import Category, Genre, Title


class TitleSerializerRead(serializers.ModelSerializer):
    """Первый сериализатор: для чтения (GET-запросов)."""

    title_name = serializers.CharField(source='name')
    year = serializers.IntegerField()
    description = serializers.CharField(required=False)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    reviews = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = ('id', 'title_name', 'year', 'description',
                  'category', 'genre', 'reviews')
        model = Title
        read_only_fields = ('author', 'reviews',)


class TitleSerializerWrite(serializers.ModelSerializer):
    """Второй сериализатор: для записи (POST-запросов)."""

    title_name = serializers.CharField(source='name')
    year = serializers.IntegerField()
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True)
    reviews = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        fields = ('id', 'title_name', 'year', 'description',
                  'category', 'genre', 'reviews')
        model = Title
        read_only_fields = ('author', 'reviews',)


    # `def validate_genres(self, value):
    #     # request = self.context['request']
    #     value = ''
    #     if isinstance(value, str) is False:
    #         raise serializers.ValidationError(
    #             'Поле "genres" должно содеражть строку/список строк.'
    #         )
    #     return value`