"""Filtersets definitions"""

from django_filters import filters, ModelMultipleChoiceFilter
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet, BaseFilterSet
from .models.host import Host
from .models.image import Image
from .models.volume import Volume
from .models.network import Network
from .models.container import Container, Env, Label, Port


class HostFilterSet(NetBoxModelFilterSet):
    """Host filterset definition class"""

    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        """Host filterset definition meta class"""

        model = Host
        fields = ("id", "name", "endpoint")

    # pylint: disable=W0613
    def search(self, queryset, name, value):
        """override"""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))


class ImageFilterSet(NetBoxModelFilterSet):
    """Image filterset definition class"""

    name = filters.CharFilter(lookup_expr="icontains")
    host_id = ModelMultipleChoiceFilter(
        field_name="host_id",
        queryset=Host.objects.all(),
        label="Host (ID)",
    )

    class Meta:
        """Image filterset definition meta class"""

        model = Image
        fields = ("id", "name", "version", "provider", "size", "ImageID")

    # pylint: disable=W0613
    def search(self, queryset, name, value):
        """override"""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))


class VolumeFilterSet(NetBoxModelFilterSet):
    """Volume filterset definition class"""

    name = filters.CharFilter(lookup_expr="icontains")
    host_id = ModelMultipleChoiceFilter(
        field_name="host_id",
        queryset=Host.objects.all(),
        label="Host (ID)",
    )

    class Meta:
        """Volume filterset definition meta class"""

        model = Volume
        fields = ("id", "name", "driver")

    # pylint: disable=W0613
    def search(self, queryset, name, value):
        """override"""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))


class NetworkFilterSet(NetBoxModelFilterSet):
    """Network filterset definition class"""

    name = filters.CharFilter(lookup_expr="icontains")
    host_id = ModelMultipleChoiceFilter(
        field_name="host_id",
        queryset=Host.objects.all(),
        label="Host (ID)",
    )

    class Meta:
        """Network filterset definition meta class"""

        model = Network
        fields = ("id", "name", "driver", "NetworkID")

    # pylint: disable=W0613
    def search(self, queryset, name, value):
        """override"""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))


class ContainerFilterSet(NetBoxModelFilterSet):
    """Container filterset definition class"""

    name = filters.CharFilter(lookup_expr="icontains")
    host_id = ModelMultipleChoiceFilter(
        field_name="host_id",
        queryset=Host.objects.all(),
        label="Host (ID)",
    )

    class Meta:
        """Container filterset definition meta class"""

        model = Container
        fields = ("id", "name")

    # pylint: disable=W0613
    def search(self, queryset, name, value):
        """override"""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))


class EnvFilterSet(BaseFilterSet):
    """Env filterset definition class"""

    container_id = ModelMultipleChoiceFilter(
        field_name="container_id",
        queryset=Container.objects.all(),
        label="Container (ID)",
    )

    class Meta:
        """Env filterset definition meta class"""

        model = Env
        fields = (
            "id",
            "var_name",
        )


class LabelFilterSet(BaseFilterSet):
    """Label filterset definition class"""

    container_id = ModelMultipleChoiceFilter(
        field_name="container_id",
        queryset=Container.objects.all(),
        label="Container (ID)",
    )

    class Meta:
        """Label filterset definition meta class"""

        model = Label
        fields = (
            "id",
            "key",
        )


class PortFilterSet(BaseFilterSet):
    """Port filterset definition class"""

    container_id = ModelMultipleChoiceFilter(
        field_name="container_id",
        queryset=Container.objects.all(),
        label="Container (ID)",
    )

    class Meta:
        """Label filterset definition meta class"""

        model = Port
        fields = (
            "id",
            "type",
        )


class MountFilterSet(BaseFilterSet):
    """Mount filterset definition class"""

    container_id = ModelMultipleChoiceFilter(
        field_name="container_id",
        queryset=Container.objects.all(),
        label="Container (ID)",
    )

    class Meta:
        """Mount filterset definition meta class"""

        model = Port
        fields = ("id",)
