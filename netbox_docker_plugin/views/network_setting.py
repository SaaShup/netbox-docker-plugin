"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.network_setting import NetworkSettingForm, NetworkSettingFilterForm
from ..models.container import NetworkSetting


class NetworkSettingListView(generic.ObjectListView):
    """NetworkSetting list view definition"""

    queryset = NetworkSetting.objects.prefetch_related("container", "network")
    table = tables.NetworkSettingTable
    filterset = filtersets.NetworkSettingFilterSet
    filterset_form = NetworkSettingFilterForm


class NetworkSettingEditView(generic.ObjectEditView):
    """NetworkSetting edition view definition"""

    queryset = NetworkSetting.objects.all()
    form = NetworkSettingForm


class NetworkSettingDeleteView(generic.ObjectDeleteView):
    """NetworkSetting delete view definition"""

    queryset = NetworkSetting.objects.all()
