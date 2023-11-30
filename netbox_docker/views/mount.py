"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.mount import MountForm
from ..models.container import Mount


class MountListView(generic.ObjectListView):
    """Mount list view definition"""

    queryset = Mount.objects.prefetch_related("volume")
    table = tables.MountTable
    filterset = filtersets.MountFilterSet


class MountEditView(generic.ObjectEditView):
    """Port edition view definition"""

    queryset = Mount.objects.all()
    form = MountForm


class MountDeleteView(generic.ObjectDeleteView):
    """Port delete view definition"""

    queryset = Mount.objects.all()
