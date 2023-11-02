"""Filtersets definitions"""

from django_filters import filters
from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q
from netbox_docker import models


class HostFilterSet(NetBoxModelFilterSet):
    """Host filterset definition class"""

    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Host
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

    class Meta:
        model = models.Image
        fields = ("id", "name", "version", "provider", "size")

    # pylint: disable=W0613
    def search(self, queryset, name, value):
        """override"""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))
