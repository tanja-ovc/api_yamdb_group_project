from rest_framework import viewsets

from ..serializers.title_serializer import TitleSerializer
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
