"""Container views definitions"""

from utilities.query import count_related
from utilities.views import ViewTab, register_model_view
from netbox.views import generic
from .. import tables, filtersets
from ..forms import container
from ..models.container import (
    Container,
    Mount,
    Bind,
    Port,
    NetworkSetting,
    Env,
    Label,
    Device,
)


@register_model_view(Container)
class ContainerView(generic.ObjectView):
    """Container view definition"""

    queryset = Container.objects.prefetch_related(
        "host",
        "image",
        "env",
        "labels",
        "mounts",
        "binds",
        "ports",
        "network_settings",
        "devices",
    )


@register_model_view(Container, name="logs", path="logs")
class ContainerLogsView(generic.ObjectView):
    """Logs tab in Container view"""

    queryset = Container.objects.all()
    tab = ViewTab(label="Logs")
    template_name = "netbox_docker_plugin/container-logs.html"


@register_model_view(Container, name="exec", path="exec")
class ContainerExecView(generic.ObjectView):
    """Exec tab in Container view"""

    queryset = Container.objects.all()
    tab = ViewTab(label="Exec")
    template_name = "netbox_docker_plugin/container-exec.html"


class ContainerNewView(generic.ObjectEditView):
    """Container edition view definition"""

    queryset = Container.objects.all()
    form = container.ContainerForm


class ContainerEditView(generic.ObjectEditView):
    """Container edition view definition"""

    queryset = Container.objects.all()
    form = container.ContainerEditForm


class ContainerListView(generic.ObjectListView):
    """Container list view definition"""

    queryset = Container.objects.annotate(
        port_count=count_related(Port, "container"),
        mount_count=count_related(Mount, "container"),
        bind_count=count_related(Bind, "container"),
        networksetting_count=count_related(NetworkSetting, "container"),
        env_count=count_related(Env, "container"),
        label_count=count_related(Label, "container"),
        device_count=count_related(Device, "container"),
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

    default_return_url = "plugins:netbox_docker_plugin:container_list"
    queryset = Container.objects.all()


class ContainerOperationView(generic.ObjectEditView):
    """Container operation view definition"""

    def get_object(self, **kwargs):
        new_kwargs = {"pk": kwargs["pk"]}
        return super().get_object(**new_kwargs)

    queryset = Container.objects.all()
    form = container.ContainerOperationForm
