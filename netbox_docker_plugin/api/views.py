"""API views definitions"""

from collections.abc import Sequence
from users.models import Token
from netbox.api.viewsets import NetBoxModelViewSet
from .. import filtersets
from .serializers import (
    HostSerializer,
    ImageSerializer,
    VolumeSerializer,
    NetworkSerializer,
    ContainerSerializer,
    RegistrySerializer,
)
from ..models.host import Host
from ..models.image import Image
from ..models.volume import Volume
from ..models.network import Network
from ..models.container import Container
from ..models.registry import Registry


class HostViewSet(NetBoxModelViewSet):
    """Host view set class"""

    queryset = Host.objects.prefetch_related(
        "images", "volumes", "networks", "containers", "registries", "tags"
    )
    filterset_class = filtersets.HostFilterSet
    serializer_class = HostSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]

    def perform_create(self, serializer):
        if isinstance(serializer.validated_data, Sequence):
            for obj in serializer.validated_data:
                token = Token(user=self.request.user, write_enabled=True)
                token.save()

                obj["token"] = token
                obj["netbox_base_url"] = self.request.stream.META["HTTP_ORIGIN"]
        else:
            token = Token(user=self.request.user, write_enabled=True)
            token.save()

            serializer.validated_data["token"] = token
            serializer.validated_data["netbox_base_url"] = self.request.stream.META[
                "HTTP_ORIGIN"
            ]

        super().perform_create(serializer)


class ImageViewSet(NetBoxModelViewSet):
    """Image view set class"""

    queryset = Image.objects.prefetch_related("host", "tags", "containers")
    filterset_class = filtersets.ImageFilterSet
    serializer_class = ImageSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class VolumeViewSet(NetBoxModelViewSet):
    """Volume view set class"""

    queryset = Volume.objects.prefetch_related("host", "tags", "mounts")
    filterset_class = filtersets.VolumeFilterSet
    serializer_class = VolumeSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class NetworkViewSet(NetBoxModelViewSet):
    """Network view set class"""

    queryset = Network.objects.prefetch_related("host", "tags", "network_settings")
    filterset_class = filtersets.NetworkFilterSet
    serializer_class = NetworkSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class ContainerViewSet(NetBoxModelViewSet):
    """Container view set class"""

    queryset = Container.objects.prefetch_related(
        "network_settings",
        "mounts",
        "binds",
        "env",
        "image",
        "host",
        "ports",
        "labels",
        "tags",
    )
    filterset_class = filtersets.ContainerFilterSet
    serializer_class = ContainerSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]


class RegistryViewSet(NetBoxModelViewSet):
    """Registry view set class"""

    queryset = Registry.objects.prefetch_related("host", "images", "tags")
    filterset_class = filtersets.RegistryFilterSet
    serializer_class = RegistrySerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]
