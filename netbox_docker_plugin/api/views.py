"""API views definitions"""

from collections.abc import Sequence
import json
import requests
from django.utils.html import escape
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from users.models import Token
from netbox.api.viewsets import NetBoxModelViewSet
from .. import filtersets
from .renderers import make_content_type_renderer
from .serializers import (
    HostSerializer,
    ImageSerializer,
    VolumeSerializer,
    NetworkSerializer,
    ContainerSerializer,
    RegistrySerializer,
    ContainerCommandSerializer,
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

    @extend_schema(
        operation_id="plugins_docker_image_force_pull",
        responses={
            (200, "application/json"): OpenApiResponse(response=str),
            (502, "application/json"): OpenApiResponse(response=str),
        },
    )
    @action(
        detail=True,
        methods=["post"],
        renderer_classes=[JSONRenderer],
    )
    def force_pull(self, _request, **_kwargs):
        """ Force pull an existing image """

        image: Image = self.get_object()
        agent_url = image.host.endpoint

        url = f"{agent_url}/api/engine/images"

        try:
            serializer = self.get_serializer(image)
            data = serializer.data
            data["force"] = True

            resp = requests.post(url, timeout=10, json={"data": data})
            resp.raise_for_status()

        except requests.HTTPError:
            return Response(
                {"success": False, "payload": resp.text},
                status=status.HTTP_502_BAD_GATEWAY,
                content_type="application/json",
            )

        return Response(
            {"success": True, "payload": resp.json()},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )


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
        "devices",
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

    @extend_schema(
        operation_id="plugins_docker_container_logs",
        responses={
            (200, "text/html"): OpenApiResponse(
                response=str,
                examples=[
                    OpenApiExample(
                        "Container's logs",
                        value="Hello World",
                        media_type="text/html",
                    ),
                ],
            ),
            (502, "text/html"): OpenApiResponse(
                response=str,
                examples=[
                    OpenApiExample(
                        "Engine error",
                        value="Error as returned by Agent",
                        media_type="text/html",
                    ),
                ],
            ),
        },
    )
    @action(
        detail=True,
        methods=["get"],
        renderer_classes=[make_content_type_renderer("text/html", "txt")],
    )
    def logs(self, _request, **_kwargs):
        """Fetch container's logs"""

        container: Container = self.get_object()
        agent_url = container.host.endpoint
        container_id = container.ContainerID

        url = f"{agent_url}/api/engine/containers/{container_id}/logs"

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()

        except requests.HTTPError:
            return Response(
                escape(resp.text),
                status=status.HTTP_502_BAD_GATEWAY,
                content_type="text/html",
            )

        return Response(
            escape(resp.text),
            status=status.HTTP_200_OK,
            content_type="text/html",
        )

    @extend_schema(
        operation_id="plugins_docker_container_exec",
        request=ContainerCommandSerializer,
        responses={
            (200, "application/json"): OpenApiResponse(
                response=str,
                examples=[
                    OpenApiExample(
                        "Command output",
                        value={"stdout": "..."},
                        media_type="application/json",
                    ),
                ],
            ),
            (502, "text/html"): OpenApiResponse(
                response=str,
                examples=[
                    OpenApiExample(
                        "Engine error",
                        value="Error as returned by Agent",
                        media_type="text/html",
                    ),
                ],
            ),
        },
    )
    @action(detail=True, methods=["post"], renderer_classes=[JSONRenderer])
    def exec(self, _request, **_kwargs):
        """Exec a command on a Container"""

        serializer = ContainerCommandSerializer(data=_request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        container: Container = self.get_object()
        agent_url = container.host.endpoint
        container_id = container.ContainerID

        url = f"{agent_url}/api/engine/containers/{container_id}/exec"

        try:
            resp = requests.put(
                url,
                data=json.dumps(serializer.validated_data),
                timeout=30,
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()

        except requests.HTTPError:
            return Response(
                escape(resp.text),
                status=status.HTTP_502_BAD_GATEWAY,
                content_type="text/html",
            )

        return Response(data=json.loads(resp.text))


class RegistryViewSet(NetBoxModelViewSet):
    """Registry view set class"""

    queryset = Registry.objects.prefetch_related("host", "images", "tags")
    filterset_class = filtersets.RegistryFilterSet
    serializer_class = RegistrySerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]
