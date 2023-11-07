"""Image views definitions"""

from netbox.views import generic
from .. import models, tables, filtersets
from ..forms import image


class ImageView(generic.ObjectView):
    """Image view definition"""

    queryset = models.Image.objects.all()


class ImageListView(generic.ObjectListView):
    """Image list view definition"""

    queryset = models.Image.objects.prefetch_related("host")
    table = tables.ImageTable
    filterset = filtersets.ImageFilterSet
    filterset_form = image.ImageFilterForm


class ImageEditView(generic.ObjectEditView):
    """Image edition view definition"""

    queryset = models.Image.objects.all()
    form = image.ImageForm


class ImageBulkEditView(generic.BulkEditView):
    """Image bulk edition view definition"""

    queryset = models.Image.objects.all()
    filterset = filtersets.ImageFilterSet
    table = tables.ImageTable
    form = image.ImageBulkEditForm


class ImageBulkImportView(generic.BulkImportView):
    """Image bulk import view definition"""

    queryset = models.Image.objects.all()
    model_form = image.ImageImportForm


class ImageDeleteView(generic.ObjectDeleteView):
    """Image delete view definition"""

    queryset = models.Image.objects.all()


class ImageBulkDeleteView(generic.BulkDeleteView):
    """Image bulk delete view definition"""

    queryset = models.Image.objects.all()
    filterset = filtersets.ImageFilterSet
    table = tables.ImageTable
