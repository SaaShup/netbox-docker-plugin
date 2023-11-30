"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.env import EnvForm
from ..models.container import Env


class EnvListView(generic.ObjectListView):
    """Env list view definition"""

    queryset = Env.objects.all()
    table = tables.EnvTable
    filterset = filtersets.EnvFilterSet


class EnvEditView(generic.ObjectEditView):
    """Env edition view definition"""

    queryset = Env.objects.all()
    form = EnvForm


class EnvDeleteView(generic.ObjectDeleteView):
    """Env delete view definition"""

    queryset = Env.objects.all()
