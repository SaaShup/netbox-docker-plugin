"""API views definitions"""

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_docker import models
from netbox_docker.api.serializers import HostSerializer


class HostViewSet(NetBoxModelViewSet):
    """Engine view set class"""

    queryset = models.Host.objects.all()
    serializer_class = HostSerializer
    http_method_names = ["get", "post", "patch", "delete"]
