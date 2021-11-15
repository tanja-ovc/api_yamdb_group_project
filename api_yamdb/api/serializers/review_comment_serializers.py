from rest_framework import serializers
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate_score(self, value):
        if not isinstance(value, int) or value not in range(1, 11):
            raise serializers.ValidationError(
                'Оценка должна быть целым числом в диапазоне от 1 до 10'
            )

        return value

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
