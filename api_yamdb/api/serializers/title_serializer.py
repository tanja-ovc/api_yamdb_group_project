from rest_framework import serializers

from reviews.models import Title


class TitleSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(slug_field='name')
    # genres = serializers.SlugRelatedField(slug_field='name')
    # reviews = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genres', 'reviews')
        model = Title
