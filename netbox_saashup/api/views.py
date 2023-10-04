"""API views definitions"""

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_saashup import models
from netbox_saashup.api.serializers import EngineSerializer


class EngineViewSet(NetBoxModelViewSet):
    """Engine view set class"""

    queryset = models.Engine.objects.all()
    serializer_class = EngineSerializer
    http_method_names = ["get", "post", "patch", "delete"]
