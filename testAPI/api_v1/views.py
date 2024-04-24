from rest_framework import viewsets
from testAPI.models import CollectionModel, LinkModel
from .serializers import CollectionSerializer, LinkSerializer
from .permissions import IsAuthorOrReadOnly


class CollectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CollectionSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return CollectionModel.objects.filter(author=self.request.user)


class LinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = LinkSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return LinkModel.objects.filter(author=self.request.user)
