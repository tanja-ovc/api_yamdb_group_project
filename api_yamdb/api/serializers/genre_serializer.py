from rest_framework import serializers

from reviews.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='name')

    class Meta:
        fields = ('genre_name', 'slug')
        model = Genre
