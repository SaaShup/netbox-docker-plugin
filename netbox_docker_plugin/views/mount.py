"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.mount import MountForm, MountFilterForm
from ..models.container import Mount


class MountListView(generic.ObjectListView):
    """Mount list view definition"""

    queryset = Mount.objects.prefetch_related("container", "volume")
    table = tables.MountTable
    filterset = filtersets.MountFilterSet
    filterset_form = MountFilterForm


class MountEditView(generic.ObjectEditView):
    """Mount edition view definition"""

    queryset = Mount.objects.all()
    form = MountForm


class MountDeleteView(generic.ObjectDeleteView):
    """Mount delete view definition"""

    queryset = Mount.objects.all()
