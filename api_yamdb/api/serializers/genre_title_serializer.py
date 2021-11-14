from rest_framework import serializers

from reviews.models import Genre, Genre_Title, Title


class Genre_TitleSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name', queryset=Title.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('id', 'title', 'genre')
        model = Genre_Title
