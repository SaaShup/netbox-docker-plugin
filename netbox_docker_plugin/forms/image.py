"""Image Forms definitions"""

from django import forms
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
)
from ..models.image import Image, ImageProviderChoices
from ..models.host import Host


class ImageForm(NetBoxModelForm):
    """Image form definition class"""

    class Meta:
        """Image form definition Meta class"""

        model = Image
        fields = (
            "host",
            "name",
            "version",
            "provider",
            "tags",
        )
        labels = {
            "name": "Name",
            "host": "Host",
            "version": "Version",
            "provider": "Provider",
        }


class ImageFilterForm(NetBoxModelFilterSetForm):
    """Image filter form definition class"""

    model = Image
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    version = forms.CharField(
        label="Version", max_length=256, min_length=1, required=False
    )
    provider = forms.ChoiceField(
        label="Provider",
        choices=ImageProviderChoices,
        required=False,
    )
    host_id = DynamicModelMultipleChoiceField(
        queryset=Host.objects.all(),
        required=False,
        label="Host",
    )
    ImageID = forms.CharField(label="ImageID", max_length=128, min_length=1, required=False)
    tag = TagFilterField(model)


class ImageImportForm(NetBoxModelImportForm):
    """Image importation form definition class"""

    version = forms.CharField(required=False, empty_value="latest")
    provider = forms.CharField(required=False, empty_value="dockerhub")
    size = forms.CharField(required=False, empty_value="0")

    class Meta:
        """Image importation form definition Meta class"""

        model = Image
        fields = ("name", "version", "provider", "host")
        labels = {
            "name": "Unique Image name",
            "version": "Image version",
            "provider": 'Image provider. Can be "dockerhub" and "github"',
            "host": "Host identifier"
        }


class ImageBulkEditForm(NetBoxModelBulkEditForm):
    """Image bulk edit form definition class"""

    version = forms.CharField(
        required=False,
    )
    provider = forms.ChoiceField(choices=ImageProviderChoices, required=False)

    model = Image
    fieldsets = (("General", ("version", "provider")),)
