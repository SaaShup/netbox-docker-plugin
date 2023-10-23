"""Model views definitions"""

from netbox.views import generic
from netbox_docker import models, tables, forms, filtersets


class HostView(generic.ObjectView):
    """Host view definition"""

    queryset = models.Host.objects.all()


class HostListView(generic.ObjectListView):
    """Host list view definition"""

    queryset = models.Host.objects.all()
    table = tables.HostTable
    filterset = filtersets.HostFilterSet
    filterset_form = forms.HostFilterForm


class HostEditView(generic.ObjectEditView):
    """Host edition view definition"""

    queryset = models.Host.objects.all()
    form = forms.HostForm


class HostBulkEditView(generic.BulkEditView):
    """Host bulk edition view definition"""

    queryset = models.Host.objects.all()
    filterset = filtersets.HostFilterSet
    table = tables.HostTable
    form = forms.HostBulkEditForm


class HostBulkImportView(generic.BulkImportView):
    """Host bulk import view definition"""

    queryset = models.Host.objects.all()
    model_form = forms.HostImportForm


class HostDeleteView(generic.ObjectDeleteView):
    """Host delete view definition"""

    queryset = models.Host.objects.all()


class HostBulkDeleteView(generic.BulkDeleteView):
    """Host bulk delete view definition"""

    queryset = models.Host.objects.all()
    filterset = filtersets.HostFilterSet
    table = tables.HostTable
