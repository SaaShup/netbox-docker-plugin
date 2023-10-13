"""API Serializer definitions"""

from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_docker import models


class HostSerializer(NetBoxModelSerializer):
    """Host Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker-api:host-detail"
    )

    class Meta:
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
        )
