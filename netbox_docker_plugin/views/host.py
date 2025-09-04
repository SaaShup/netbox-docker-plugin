"""Host views definitions"""

from users.models import Token
from utilities.query import count_related
from utilities.views import ViewTab, GetRelatedModelsMixin, register_model_view
from netbox.views import generic
from .. import tables, filtersets
from ..forms import host
from ..models.host import Host
from ..models.image import Image
from ..models.volume import Volume
from ..models.network import Network
from ..models.container import Container
from ..models.registry import Registry


@register_model_view(Host)
class HostView(GetRelatedModelsMixin, generic.ObjectView):
    """Host view definition"""

    queryset = Host.objects.prefetch_related(
        "images", "volumes", "networks", "containers", "registries"
    )

    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(
                request,
                instance,
                omit=(),
                extra=(),
            ),
        }


@register_model_view(Host, name="graph", path="graph")
class HostGraphView(generic.ObjectView):
    """Logs tab in Container view"""

    queryset = Host.objects.all()
    tab = ViewTab(label="Graph")
    template_name = "netbox_docker_plugin/host-graph.html"


class HostListView(generic.ObjectListView):
    """Host list view definition"""

    queryset = Host.objects.annotate(
        image_count=count_related(Image, "host"),
        volume_count=count_related(Volume, "host"),
        network_count=count_related(Network, "host"),
        container_count=count_related(Container, "host"),
        registry_count=count_related(Registry, "host"),
    )
    table = tables.HostTable
    filterset = filtersets.HostFilterSet
    filterset_form = host.HostFilterForm


class HostEditView(generic.ObjectEditView):
    """Host edition view definition"""

    queryset = Host.objects.all()
    form = host.HostForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if request.method == "POST" and not "pk" in url_kwargs:
            token = Token(user=self.request.user, write_enabled=True)
            token.save()

            obj.token = token
            obj.netbox_base_url = request.META["HTTP_ORIGIN"]

        return super().alter_object(obj, request, url_args, url_kwargs)


class HostBulkEditView(generic.BulkEditView):
    """Host bulk edition view definition"""

    queryset = Host.objects.all()
    filterset = filtersets.HostFilterSet
    table = tables.HostTable
    form = host.HostBulkEditForm


class HostBulkImportView(generic.BulkImportView):
    """Host bulk import view definition"""

    queryset = Host.objects.all()
    model_form = host.HostImportForm

    def save_object(self, object_form, request):
        token = Token(user=request.user, write_enabled=True)
        token.save()

        object_form.instance.token = token
        object_form.instance.netbox_base_url = request.META["HTTP_ORIGIN"]

        return super().save_object(object_form, request)


class HostDeleteView(generic.ObjectDeleteView):
    """Host delete view definition"""

    default_return_url = "plugins:netbox_docker_plugin:host_list"
    queryset = Host.objects.all()


class HostBulkDeleteView(generic.BulkDeleteView):
    """Host bulk delete view definition"""

    queryset = Host.objects.all()
    filterset = filtersets.HostFilterSet
    table = tables.HostTable


class HostOperationView(generic.ObjectEditView):
    """Host operation view definition"""

    def get_object(self, **kwargs):
        new_kwargs = {"pk": kwargs["pk"]}
        return super().get_object(**new_kwargs)

    queryset = Host.objects.all()
    form = host.HostOperationForm
