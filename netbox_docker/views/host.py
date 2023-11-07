"""Host views definitions"""

from utilities.utils import count_related
from netbox.views import generic
from .. import models, tables, filtersets
from ..forms import host


class HostView(generic.ObjectView):
    """Host view definition"""

    queryset = models.Host.objects.prefetch_related("images", "volumes", "networks")

    def get_extra_context(self, request, instance):
        related_models = (
            (
                models.Image.objects.filter(host=instance),
                "host_id",
            ),
            (
                models.Volume.objects.filter(host=instance),
                "host_id",
            ),
            (
                models.Network.objects.filter(host=instance),
                "host_id",
            ),
        )

        return {
            "related_models": related_models,
        }


class HostListView(generic.ObjectListView):
    """Host list view definition"""

    queryset = models.Host.objects.annotate(
        image_count=count_related(models.Image, "host"),
        volume_count=count_related(models.Volume, "host"),
        network_count=count_related(models.Network, "host"),
    )
    table = tables.HostTable
    filterset = filtersets.HostFilterSet
    filterset_form = host.HostFilterForm


class HostEditView(generic.ObjectEditView):
    """Host edition view definition"""

    queryset = models.Host.objects.all()
    form = host.HostForm


class HostBulkEditView(generic.BulkEditView):
    """Host bulk edition view definition"""

    queryset = models.Host.objects.all()
    filterset = filtersets.HostFilterSet
    table = tables.HostTable
    form = host.HostBulkEditForm


class HostBulkImportView(generic.BulkImportView):
    """Host bulk import view definition"""

    queryset = models.Host.objects.all()
    model_form = host.HostImportForm


class HostDeleteView(generic.ObjectDeleteView):
    """Host delete view definition"""

    queryset = models.Host.objects.all()


class HostBulkDeleteView(generic.BulkDeleteView):
    """Host bulk delete view definition"""

    queryset = models.Host.objects.all()
    filterset = filtersets.HostFilterSet
    table = tables.HostTable
