"""API Serializer definitions"""

from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models.host import Host
from ..models.image import Image
from ..models.volume import Volume
from ..models.network import Network


class NestedHostSerializer(WritableNestedSerializer):
    """Nested Host Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:host-detail"
    )

    class Meta:
        """Nested Host Serializer Meta class"""

        model = Host
        fields = ("id", "url", "display", "endpoint", "name")


class NestedImageSerializer(WritableNestedSerializer):
    """Nested Image Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:image-detail"
    )

    class Meta:
        """Nested Image Serializer Meta class"""

        model = Image
        fields = (
            "id",
            "url",
            "name",
            "version",
            "provider",
            "size",
        )


class NestedVolumeSerializer(WritableNestedSerializer):
    """Nested Volume Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:volume-detail"
    )

    class Meta:
        """Nested Volume Serializer Meta class"""

        model = Volume
        fields = (
            "id",
            "url",
            "name",
            "driver",
        )


class NestedNetworkSerializer(WritableNestedSerializer):
    """Nested Network Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:network-detail"
    )

    class Meta:
        """Nested Network Serializer Meta class"""

        model = Network
        fields = (
            "id",
            "url",
            "name",
            "driver",
        )


class ImageSerializer(NetBoxModelSerializer):
    """Image Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:image-detail"
    )
    host = NestedHostSerializer()

    class Meta:
        """Image Serializer Meta class"""

        model = Image
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


class VolumeSerializer(NetBoxModelSerializer):
    """Volume Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:volume-detail"
    )
    host = NestedHostSerializer()

    class Meta:
        """Volume Serializer Meta class"""

        model = Volume
        fields = (
            "id",
            "url",
            "host",
            "name",
            "driver",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
        )


class NetworkSerializer(NetBoxModelSerializer):
    """Network Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:network-detail"
    )
    host = NestedHostSerializer()

    class Meta:
        """Network Serializer Meta class"""

        model = Network
        fields = (
            "id",
            "url",
            "host",
            "name",
            "driver",
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
    volumes = NestedVolumeSerializer(many=True, read_only=True)
    networks = NestedNetworkSerializer(many=True, read_only=True)

    class Meta:
        """Host Serializer Meta class"""

        model = Host
        fields = (
            "id",
            "url",
            "display",
            "endpoint",
            "name",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
            "images",
            "volumes",
            "networks",
        )
