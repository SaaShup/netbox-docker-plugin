"""Container views definitions"""

from netbox.views import generic
from .. import tables, filtersets
from ..forms import container
from ..models.container import Container


class ContainerView(generic.ObjectView):
    """Container view definition"""

    queryset = Container.objects.prefetch_related(
        "host", "image", "env", "labels", "mounts", "ports", "network_settings"
    )


class ContainerEditView(generic.ObjectEditView):
    """Container edition view definition"""

    queryset = Container.objects.all()
    form = container.ContainerForm


class ContainerListView(generic.ObjectListView):
    """Container list view definition"""

    queryset = Container.objects.prefetch_related("host")
    table = tables.ContainerTable
    filterset = filtersets.ContainerFilterSet
    filterset_form = container.ContainerFilterForm


class ContainerBulkImportView(generic.BulkImportView):
    """Container bulk import view definition"""

    queryset = Container.objects.all()
    model_form = container.ContainerImportForm


class ContainerBulkEditView(generic.BulkEditView):
    """Container bulk edition view definition"""

    queryset = Container.objects.all()
    filterset = filtersets.ContainerFilterSet
    table = tables.ContainerTable
    form = container.ContainerBulkEditForm


class ContainerBulkDeleteView(generic.BulkDeleteView):
    """Container bulk delete view definition"""

    queryset = Container.objects.all()
    filterset = filtersets.ContainerFilterSet
    table = tables.ContainerTable


class ContainerDeleteView(generic.ObjectDeleteView):
    """Container delete view definition"""

    queryset = Container.objects.all()
