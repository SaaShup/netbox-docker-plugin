"""Container views definitions"""

from collections import defaultdict
from django.db import router
from django.db.models.deletion import Collector
from extras.models import JournalEntry
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


class MinContainerListView(generic.ObjectListView):
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

    table = tables.MinContainerTable
    filterset = filtersets.ContainerFilterSet


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


class _JournalEntryCount:
    """Proxy passed to the deletion template in place of a full JournalEntry list.

    The template calls len() for the accordion header count, then iterates to
    render individual rows. This object answers len() with a single COUNT query
    and yields nothing on iteration, avoiding fetching hundreds of thousands of
    rows just to display a number."""

    def __init__(self, queryset):
        self._queryset = queryset
        self._count = None

    def __len__(self):
        if self._count is None:
            self._count = self._queryset.count()
        return self._count

    def __iter__(self):
        return iter([])

    def __bool__(self):
        return len(self) > 0


class ContainerDeleteView(generic.ObjectDeleteView):
    """Container delete view definition"""

    default_return_url = "plugins:netbox_docker_plugin:container_list"
    queryset = Container.objects.select_related("host", "image")

    def _get_dependent_objects(self, obj):
        class SkipJournalCollector(Collector):
            """Collector that skips JournalEntry to avoid a slow full scan."""

            def collect(self, objs, **kwargs):  # pylint: disable=arguments-differ
                if getattr(objs, "model", None) is JournalEntry:
                    return
                super().collect(objs, **kwargs)

        using = router.db_for_write(obj._meta.model)
        collector = SkipJournalCollector(using=using)
        collector.collect([obj])

        dependent_objects = defaultdict(list)
        for model, instances in collector.instances_with_model():
            if model._meta.auto_created:
                continue
            if instances == obj:
                continue
            dependent_objects[model].append(instances)

        journal_qs = JournalEntry.objects.filter(
            assigned_object_type__app_label="netbox_docker_plugin",
            assigned_object_type__model="container",
            assigned_object_id=obj.pk,
        )
        if journal_qs.exists():
            dependent_objects[JournalEntry] = _JournalEntryCount(journal_qs)

        return dict(dependent_objects)


class ContainerOperationView(generic.ObjectEditView):
    """Container operation view definition"""

    def get_object(self, **kwargs):
        new_kwargs = {"pk": kwargs["pk"]}
        return super().get_object(**new_kwargs)

    queryset = Container.objects.all()
    form = container.ContainerOperationForm
