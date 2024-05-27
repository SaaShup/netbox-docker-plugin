"""Network views definitions"""

from utilities.query import count_related
from netbox.views import generic
from .. import tables, filtersets
from ..forms import network
from ..models.network import Network
from ..models.container import NetworkSetting

class NetworkView(generic.ObjectView):
    """Network view definition"""

    queryset = Network.objects.all()


class NetworkListView(generic.ObjectListView):
    """Network list view definition"""

    queryset = Network.objects.annotate(
        networksetting_count=count_related(NetworkSetting, "network"),
    )
    table = tables.NetworkTable
    filterset = filtersets.NetworkFilterSet
    filterset_form = network.NetworkFilterForm


class NetworkEditView(generic.ObjectEditView):
    """Network edition view definition"""

    queryset = Network.objects.all()
    form = network.NetworkForm


class NetworkBulkEditView(generic.BulkEditView):
    """Network bulk edition view definition"""

    queryset = Network.objects.all()
    filterset = filtersets.NetworkFilterSet
    table = tables.NetworkTable
    form = network.NetworkBulkEditForm


class NetworkBulkImportView(generic.BulkImportView):
    """Network bulk import view definition"""

    queryset = Network.objects.all()
    model_form = network.NetworkImportForm


class NetworkDeleteView(generic.ObjectDeleteView):
    """Network delete view definition"""

    default_return_url = "plugins:netbox_docker_plugin:network_list"
    queryset = Network.objects.all()


class NetworkBulkDeleteView(generic.BulkDeleteView):
    """Network bulk delete view definition"""

    queryset = Network.objects.all()
    filterset = filtersets.NetworkFilterSet
    table = tables.NetworkTable
