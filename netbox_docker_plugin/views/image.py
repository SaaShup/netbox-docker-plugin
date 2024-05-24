"""Image views definitions"""

from utilities.query import count_related
from netbox.views import generic
from .. import tables, filtersets
from ..forms import image
from ..models.image import Image
from ..models.container import Container


class ImageView(generic.ObjectView):
    """Image view definition"""

    queryset = Image.objects.all()


class ImageListView(generic.ObjectListView):
    """Image list view definition"""

    queryset = Image.objects.annotate(
        container_count=count_related(Container, "image"),
    )
    table = tables.ImageTable
    filterset = filtersets.ImageFilterSet
    filterset_form = image.ImageFilterForm


class ImageEditView(generic.ObjectEditView):
    """Image edition view definition"""

    queryset = Image.objects.all()
    form = image.ImageForm


class ImageBulkEditView(generic.BulkEditView):
    """Image bulk edition view definition"""

    queryset = Image.objects.all()
    filterset = filtersets.ImageFilterSet
    table = tables.ImageTable
    form = image.ImageBulkEditForm


class ImageBulkImportView(generic.BulkImportView):
    """Image bulk import view definition"""

    queryset = Image.objects.all()
    model_form = image.ImageImportForm


class ImageDeleteView(generic.ObjectDeleteView):
    """Image delete view definition"""

    default_return_url = "plugins:netbox_docker_plugin:image_list"
    queryset = Image.objects.all()


class ImageBulkDeleteView(generic.BulkDeleteView):
    """Image bulk delete view definition"""

    queryset = Image.objects.all()
    filterset = filtersets.ImageFilterSet
    table = tables.ImageTable
