"""Model views definitions"""

from utilities.utils import count_related
from utilities.views import ViewTab, register_model_view
from netbox.views import generic
from netbox_docker import models, tables, forms, filtersets


class HostView(generic.ObjectView):
    """Host view definition"""

    queryset = models.Host.objects.prefetch_related("images")

    def get_extra_context(self, request, instance):
        related_models = (
            (
                models.Image.objects.filter(host=instance),
                "host_id",
            ),
        )

        return {
            "related_models": related_models,
        }


class HostListView(generic.ObjectListView):
    """Host list view definition"""

    queryset = models.Host.objects.annotate(
        image_count=count_related(models.Image, "host")
    )
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


class ImageView(generic.ObjectView):
    """Image view definition"""

    queryset = models.Image.objects.all()


class ImageListView(generic.ObjectListView):
    """Image list view definition"""

    queryset = models.Image.objects.all()
    table = tables.ImageTable
    filterset = filtersets.ImageFilterSet
    filterset_form = forms.ImageFilterForm


class ImageEditView(generic.ObjectEditView):
    """Image edition view definition"""

    queryset = models.Image.objects.all()
    form = forms.ImageForm


class ImageBulkEditView(generic.BulkEditView):
    """Image bulk edition view definition"""

    queryset = models.Image.objects.all()
    # filterset = filtersets.HostFilterSet
    table = tables.ImageTable
    form = forms.ImageBulkEditForm


class ImageBulkImportView(generic.BulkImportView):
    """Image bulk import view definition"""

    queryset = models.Image.objects.all()
    model_form = forms.ImageImportForm


class ImageDeleteView(generic.ObjectDeleteView):
    """Image delete view definition"""

    queryset = models.Image.objects.all()


class ImageBulkDeleteView(generic.BulkDeleteView):
    """Image bulk delete view definition"""

    queryset = models.Image.objects.all()
    # filterset = filtersets.ImageFilterSet
    table = tables.ImageTable
