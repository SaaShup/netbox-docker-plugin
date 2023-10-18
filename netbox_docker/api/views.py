"""API views definitions"""

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_docker import models
from netbox_docker.api.serializers import HostSerializer, ImageSerializer


class HostViewSet(NetBoxModelViewSet):
    """Host view set class"""

    queryset = models.Host.objects.prefetch_related("images", "tags").all()
    serializer_class = HostSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class ImageViewSet(NetBoxModelViewSet):
    """Image view set class"""

    queryset = models.Image.objects.prefetch_related("host", "tags").all()
    serializer_class = ImageSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]
