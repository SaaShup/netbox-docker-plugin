"""Registry views definitions"""

from utilities.query import count_related
from utilities.views import GetRelatedModelsMixin
from netbox.views import generic
from .. import tables, filtersets
from ..forms import registry
from ..models.image import Image
from ..models.registry import Registry


class RegistryView(GetRelatedModelsMixin, generic.ObjectView):
    """Registry view definition"""

    queryset = Registry.objects.prefetch_related("images")

    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(
                request,
                instance,
                omit=(),
                extra=(),
            ),
        }


class RegistryListView(generic.ObjectListView):
    """Registry list view definition"""

    queryset = Registry.objects.annotate(
        image_count=count_related(Image, "registry"),
    )
    table = tables.RegistryTable
    filterset = filtersets.RegistryFilterSet
    filterset_form = registry.RegistryFilterForm


class RegistryEditView(generic.ObjectEditView):
    """Registry edition view definition"""

    queryset = Registry.objects.all()
    form = registry.RegistryForm


class RegistryDeleteView(generic.ObjectDeleteView):
    """Registry delete view definition"""

    queryset = Registry.objects.all()


class RegistryBulkDeleteView(generic.BulkDeleteView):
    """Registry bulk delete view definition"""

    queryset = Registry.objects.all()
    filterset = filtersets.RegistryFilterSet
    table = tables.RegistryTable
