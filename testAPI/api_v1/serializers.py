from rest_framework import serializers
from testAPI.models import CollectionModel, LinkModel


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
            "description",
        )
        model = CollectionModel


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "url",
            "collection",
            "author",
            "title",
            "description",
        )
        model = LinkModel


