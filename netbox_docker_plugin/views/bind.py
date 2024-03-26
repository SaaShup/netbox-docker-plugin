"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.bind import BindForm, BindFilterForm
from ..models.container import Bind


class BindListView(generic.ObjectListView):
    """Bind list view definition"""

    queryset = Bind.objects.prefetch_related("container")
    table = tables.BindTable
    filterset = filtersets.BindFilterSet
    filterset_form = BindFilterForm


class BindEditView(generic.ObjectEditView):
    """Bind edition view definition"""

    queryset = Bind.objects.all()
    form = BindForm


class BindDeleteView(generic.ObjectDeleteView):
    """Bind delete view definition"""

    queryset = Bind.objects.all()
