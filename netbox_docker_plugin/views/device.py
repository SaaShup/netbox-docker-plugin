"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.device import DeviceForm, DeviceFilterForm
from ..models.container import Device


class DeviceListView(generic.ObjectListView):
    """Device list view definition"""

    queryset = Device.objects.prefetch_related("container")
    table = tables.DeviceTable
    filterset = filtersets.DeviceFilterSet
    filterset_form = DeviceFilterForm


class DeviceEditView(generic.ObjectEditView):
    """Device edition view definition"""

    queryset = Device.objects.all()
    form = DeviceForm


class DeviceDeleteView(generic.ObjectDeleteView):
    """Device delete view definition"""

    queryset = Device.objects.all()
