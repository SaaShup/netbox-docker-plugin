"""Network views definitions"""

from netbox.views import generic
from .. import models, tables, filtersets
from ..forms import network


class NetworkView(generic.ObjectView):
    """Network view definition"""

    queryset = models.Network.objects.all()


class NetworkListView(generic.ObjectListView):
    """Network list view definition"""

    queryset = models.Network.objects.prefetch_related("host")
    table = tables.NetworkTable
    filterset = filtersets.NetworkFilterSet
    filterset_form = network.NetworkFilterForm


class NetworkEditView(generic.ObjectEditView):
    """Network edition view definition"""

    queryset = models.Network.objects.all()
    form = network.NetworkForm


class NetworkBulkEditView(generic.BulkEditView):
    """Network bulk edition view definition"""

    queryset = models.Network.objects.all()
    filterset = filtersets.NetworkFilterSet
    table = tables.NetworkTable
    form = network.NetworkBulkEditForm


class NetworkBulkImportView(generic.BulkImportView):
    """Network bulk import view definition"""

    queryset = models.Network.objects.all()
    model_form = network.NetworkImportForm


class NetworkDeleteView(generic.ObjectDeleteView):
    """Network delete view definition"""

    queryset = models.Network.objects.all()


class NetworkBulkDeleteView(generic.BulkDeleteView):
    """Network bulk delete view definition"""

    queryset = models.Network.objects.all()
    filterset = filtersets.NetworkFilterSet
    table = tables.NetworkTable
