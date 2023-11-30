"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.port import PortForm
from ..models.container import Port


class PortListView(generic.ObjectListView):
    """Port list view definition"""

    queryset = Port.objects.all()
    table = tables.PortTable
    filterset = filtersets.PortFilterSet


class PortEditView(generic.ObjectEditView):
    """Port edition view definition"""

    queryset = Port.objects.all()
    form = PortForm


class PortDeleteView(generic.ObjectDeleteView):
    """Port delete view definition"""

    queryset = Port.objects.all()
