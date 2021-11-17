import statistics

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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        if obj.reviews.exists():
            this_title_reviews = obj.reviews.all()
            scores_list = []
            for review in this_title_reviews:
                scores_list.append(review.score)
            rating = statistics.mean(scores_list)
            return rating
        return None
