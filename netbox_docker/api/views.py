"""API views definitions"""

from netbox.api.viewsets import NetBoxModelViewSet
from .. import models
from .serializers import HostSerializer, ImageSerializer, VolumeSerializer


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


class VolumeViewSet(NetBoxModelViewSet):
    """Volume view set class"""

    queryset = models.Volume.objects.prefetch_related("host", "tags").all()
    serializer_class = VolumeSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]
