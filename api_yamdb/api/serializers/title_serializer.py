from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "name": value.name,
            "slug": value.slug
        }

    def to_internal_value(self, data):
        return Category.objects.get(slug=data)


class GenreListField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "name": value.name,
            "slug": value.slug
        }

    def to_internal_value(self, data):
        return Genre.objects.get(slug=data)


class TitleSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    category = CategoryField(queryset=Category.objects.all())
    genre = GenreListField(queryset=Genre.objects.all(), many=True)
    # rating field to be added

    class Meta:
        # rating field to be added
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')
        model = Title
