"""API views definitions"""

from netbox.api.viewsets import NetBoxModelViewSet
from .. import filtersets
from .serializers import (
    HostSerializer,
    ImageSerializer,
    VolumeSerializer,
    NetworkSerializer,
    ContainerSerializer,
)
from ..models.host import Host
from ..models.image import Image
from ..models.volume import Volume
from ..models.network import Network
from ..models.container import Container


class HostViewSet(NetBoxModelViewSet):
    """Host view set class"""

    queryset = Host.objects.prefetch_related("images", "volumes", "tags")
    filterset_class = filtersets.HostFilterSet
    serializer_class = HostSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class ImageViewSet(NetBoxModelViewSet):
    """Image view set class"""

    queryset = Image.objects.prefetch_related("host", "tags")
    filterset_class = filtersets.ImageFilterSet
    serializer_class = ImageSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class VolumeViewSet(NetBoxModelViewSet):
    """Volume view set class"""

    queryset = Volume.objects.prefetch_related("host", "tags")
    filterset_class = filtersets.VolumeFilterSet
    serializer_class = VolumeSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class NetworkViewSet(NetBoxModelViewSet):
    """Network view set class"""

    queryset = Network.objects.prefetch_related("host", "tags")
    filterset_class = filtersets.NetworkFilterSet
    serializer_class = NetworkSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class ContainerViewSet(NetBoxModelViewSet):
    """Container view set class"""

    queryset = Container.objects.all()
    filterset_class = filtersets.ContainerFilterSet
    serializer_class = ContainerSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]
