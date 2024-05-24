"""Volume views definitions"""

from utilities.query import count_related
from netbox.views import generic
from .. import tables, filtersets
from ..forms import volume
from ..models.volume import Volume
from ..models.container import Mount


class VolumeView(generic.ObjectView):
    """Volume view definition"""

    queryset = Volume.objects.all()


class VolumeEditView(generic.ObjectEditView):
    """Volume edition view definition"""

    queryset = Volume.objects.all()
    form = volume.VolumeForm


class VolumeListView(generic.ObjectListView):
    """Volume list view definition"""

    queryset = Volume.objects.annotate(
        mount_count=count_related(Mount, "volume"),
    )
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

    default_return_url = "plugins:netbox_docker_plugin:volume_list"
    queryset = Volume.objects.all()
