from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.permissions import AdminOrReadOnly
from api.serializers.title_serializer import (TitleSerializerRead,
                                              TitleSerializerWrite)
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleSerializer

    # !!! change back to AdminOrReadOnly later !!!
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name', 'year', 'category__slug', 'genre__slug'
    )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TitleSerializerWrite
        return TitleSerializerRead
