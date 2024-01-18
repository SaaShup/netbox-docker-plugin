"""Host views definitions"""

from users.models import Token
from utilities.utils import count_related
from netbox.views import generic
from .. import tables, filtersets
from ..forms import host
from ..models.host import Host
from ..models.image import Image
from ..models.volume import Volume
from ..models.network import Network
from ..models.container import Container


class HostView(generic.ObjectView):
    """Host view definition"""

    queryset = Host.objects.prefetch_related(
        "images", "volumes", "networks", "containers"
    )

    def get_extra_context(self, request, instance):
        related_models = (
            (
                Image.objects.filter(host=instance),
                "host_id",
            ),
            (
                Volume.objects.filter(host=instance),
                "host_id",
            ),
            (
                Network.objects.filter(host=instance),
                "host_id",
            ),
            (
                Container.objects.filter(host=instance),
                "host_id",
            ),
        )

        return {
            "related_models": related_models,
        }


class HostListView(generic.ObjectListView):
    """Host list view definition"""

    queryset = Host.objects.annotate(
        image_count=count_related(Image, "host"),
        volume_count=count_related(Volume, "host"),
        network_count=count_related(Network, "host"),
        container_count=count_related(Container, "host"),
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

    queryset = Host.objects.all()


class HostBulkDeleteView(generic.BulkDeleteView):
    """Host bulk delete view definition"""

    queryset = Host.objects.all()
    filterset = filtersets.HostFilterSet
    table = tables.HostTable
