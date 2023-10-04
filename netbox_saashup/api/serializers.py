"""API Serializer definitions"""

from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_saashup import models


class EngineSerializer(NetBoxModelSerializer):
    """Engine Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_saashup-api:engine-detail"
    )

    class Meta:
        model = models.Engine
        fields = (
            "id",
            "url",
            "domain",
            "port",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
        )
