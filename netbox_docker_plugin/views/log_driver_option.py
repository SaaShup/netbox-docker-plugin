"""Log driver option views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.log_driver_option import LogDriverOptionForm
from ..models.container import LogDriverOption


class LogDriverOptionListView(generic.ObjectListView):
    """Log driver option list view definition"""

    queryset = LogDriverOption.objects.all()
    table = tables.LogDriverOptionTable
    filterset = filtersets.LogDriverOptionFilterSet


class LogDriverOptionEditView(generic.ObjectEditView):
    """Log driver option edition view definition"""

    queryset = LogDriverOption.objects.all()
    form = LogDriverOptionForm


class LogDriverOptionDeleteView(generic.ObjectDeleteView):
    """Log driver option delete view definition"""

    queryset = LogDriverOption.objects.all()
