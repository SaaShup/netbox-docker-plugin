"""Registry views definitions"""

from utilities.utils import count_related
from netbox.views import generic
from .. import tables, filtersets
from ..forms import registry
from ..models.image import Image
from ..models.registry import Registry


class RegistryView(generic.ObjectView):
    """Registry view definition"""

    queryset = Registry.objects.prefetch_related("images")

    def get_extra_context(self, request, instance):
        related_models = (
            (
                Image.objects.filter(registry=instance),
                "registry_id",
            ),
        )

        return {
            "related_models": related_models,
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
