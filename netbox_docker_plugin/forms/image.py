"""Image Forms definitions"""

from django import forms
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
)
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
)
from ..models.image import Image
from ..models.host import Host
from ..models.registry import Registry


class ImageForm(NetBoxModelForm):
    """Image form definition class"""

    host = DynamicModelChoiceField(
        label="Host", queryset=Host.objects.all(), required=True
    )
    registry = DynamicModelChoiceField(
        label="Registry",
        queryset=Registry.objects.all(),
        required=True,
        query_params={"host_id": "$host"},
    )

    class Meta:
        """Image form definition Meta class"""

        model = Image
        fields = (
            "host",
            "registry",
            "name",
            "version",
            "tags",
        )
        labels = {
            "name": "Name",
            "host": "Host",
            "registry": "Registry",
            "version": "Version",
        }


class ImageFilterForm(NetBoxModelFilterSetForm):
    """Image filter form definition class"""

    model = Image
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    version = forms.CharField(
        label="Version", max_length=256, min_length=1, required=False
    )
    registry_id = DynamicModelMultipleChoiceField(
        queryset=Registry.objects.all(),
        required=False,
        label="Registry",
    )
    host_id = DynamicModelMultipleChoiceField(
        queryset=Host.objects.all(),
        required=False,
        label="Host",
    )
    ImageID = forms.CharField(
        label="ImageID", max_length=128, min_length=1, required=False
    )
    tag = TagFilterField(model)


class ImageImportForm(NetBoxModelImportForm):
    """Image importation form definition class"""

    version = forms.CharField(
        required=False, empty_value="latest", help_text="Image version"
    )
    size = forms.CharField(required=False, empty_value="0", help_text="In MBytes")

    class Meta:
        """Image importation form definition Meta class"""

        model = Image
        fields = ("name", "version", "registry", "host")
        labels = {
            "name": "Unique Image name",
            "host": "Host identifier",
            "registry": "Image registry. Default value `dockerhub`.",
        }


class ImageBulkEditForm(NetBoxModelBulkEditForm):
    """Image bulk edit form definition class"""

    version = forms.CharField(
        required=False,
    )

    model = Image
    fieldsets = (FieldSet("version", name="General"),)
