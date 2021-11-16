from rest_framework import serializers

from reviews.models import Genre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
