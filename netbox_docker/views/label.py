"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms.label import LabelForm
from ..models.container import Label


class LabelListView(generic.ObjectListView):
    """Label list view definition"""

    queryset = Label.objects.all()
    table = tables.LabelTable
    filterset = filtersets.LabelFilterSet


class LabelEditView(generic.ObjectEditView):
    """Label edition view definition"""

    queryset = Label.objects.all()
    form = LabelForm


class LabelDeleteView(generic.ObjectDeleteView):
    """Label delete view definition"""

    queryset = Label.objects.all()
