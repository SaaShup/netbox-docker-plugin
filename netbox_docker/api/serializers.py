"""API Serializer definitions"""

from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from .. import models


class NestedHostSerializer(WritableNestedSerializer):
    """Nested Host Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:host-detail"
    )

    class Meta:
        """Nested Host Serializer Meta class"""

        model = models.Host
        fields = ("id", "url", "endpoint", "name")


class NestedImageSerializer(WritableNestedSerializer):
    """Nested Image Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:image-detail"
    )

    class Meta:
        """Nested Image Serializer Meta class"""

        model = models.Image
        fields = (
            "id",
            "url",
            "name",
            "version",
            "provider",
            "size",
        )


class ImageSerializer(NetBoxModelSerializer):
    """Image Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:image-detail"
    )
    host = NestedHostSerializer()

    class Meta:
        """Image Serializer Meta class"""

        model = models.Image
        fields = (
            "id",
            "url",
            "host",
            "name",
            "version",
            "provider",
            "size",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
        )


class HostSerializer(NetBoxModelSerializer):
    """Host Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:host-detail"
    )
    images = NestedImageSerializer(many=True, read_only=True)

    class Meta:
        """Host Serializer Meta class"""

        model = models.Host
        fields = (
            "id",
            "url",
            "endpoint",
            "name",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
            "images",
        )
