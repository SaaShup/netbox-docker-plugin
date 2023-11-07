"""Filtersets definitions"""

from django_filters import filters, ModelMultipleChoiceFilter
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models.host import Host
from .models.image import Image
from .models.volume import Volume
from .models.network import Network


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
        fields = ("id", "name", "version", "provider", "size")

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
        fields = ("id", "name", "driver")

    # pylint: disable=W0613
    def search(self, queryset, name, value):
        """override"""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))
