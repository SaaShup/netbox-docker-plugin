"""Container views definitions"""

from utilities.utils import count_related
from netbox.views import generic
from .. import tables, filtersets
from ..forms import container
from ..models.container import Container, Mount, Port, NetworkSetting, Env, Label


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

    queryset = Container.objects.annotate(
        port_count=count_related(Port, "container"),
        mount_count=count_related(Mount, "container"),
        networksetting_count=count_related(NetworkSetting, "container"),
        env_count=count_related(Env, "container"),
        label_count=count_related(Label, "container"),
    )

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


class ContainerOperationView(generic.ObjectEditView):
    """Container operation view definition"""

    def get_object(self, **kwargs):
        new_kwargs = {"pk": kwargs["pk"]}
        return super().get_object(**new_kwargs)

    queryset = Container.objects.all()
    form = container.ContainerOperationForm
