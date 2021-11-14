from rest_framework import viewsets

from api.serializers.title_serializer import (TitleSerializer,
                                              TitleSerializerWrite)
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TitleSerializerWrite
        return TitleSerializer
