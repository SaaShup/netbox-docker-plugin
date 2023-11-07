"""Volume views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms import volume
from ..models.volume import Volume


class VolumeView(generic.ObjectView):
    """Volume view definition"""

    queryset = Volume.objects.all()


class VolumeEditView(generic.ObjectEditView):
    """Volume edition view definition"""

    queryset = Volume.objects.all()
    form = volume.VolumeForm


class VolumeListView(generic.ObjectListView):
    """Volume list view definition"""

    queryset = Volume.objects.prefetch_related("host")
    table = tables.VolumeTable
    filterset = filtersets.VolumeFilterSet
    filterset_form = volume.VolumeFilterForm


class VolumeBulkImportView(generic.BulkImportView):
    """Volume bulk import view definition"""

    queryset = Volume.objects.all()
    model_form = volume.VolumeImportForm


class VolumeBulkDeleteView(generic.BulkDeleteView):
    """Volume bulk delete view definition"""

    queryset = Volume.objects.all()
    filterset = filtersets.VolumeFilterSet
    table = tables.VolumeTable


class VolumeDeleteView(generic.ObjectDeleteView):
    """Volume delete view definition"""

    queryset = Volume.objects.all()
