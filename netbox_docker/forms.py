"""Forms definitions"""

from django import forms
from utilities.forms.fields import TagFilterField
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
)
from . import models


class HostForm(NetBoxModelForm):
    """Host form definition class"""

    class Meta:
        """Host form definition Meta class"""

        model = models.Host
        fields = (
            "name",
            "endpoint",
            "tags",
        )
        help_texts = {"name": "Unique Name", "endpoint": "Docker instance endpoint"}
        labels = {"name": "Name", "endpoint": "Endpoint"}


class HostFilterForm(NetBoxModelFilterSetForm):
    """Host filter form definition class"""

    model = models.Host
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    endpoint = forms.CharField(
        label="Endpoint", max_length=256, min_length=1, required=False
    )
    tag = TagFilterField(model)


class HostImportForm(NetBoxModelImportForm):
    """Host importation form definition class"""

    class Meta:
        """Host importation form definition Meta class"""

        model = models.Host
        fields = (
            "name",
            "endpoint",
        )
        labels = {
            "name": "Unique name",
            "endpoint": "Docker instance URL",
        }


class HostBulkEditForm(NetBoxModelBulkEditForm):
    """Host bulk edit form definition class"""

    endpoint = forms.CharField(
        required=False,
    )

    model = models.Host
    fieldsets = (("General", ("endpoint",)),)


class ImageForm(NetBoxModelForm):
    """Image form definition class"""

    class Meta:
        """Image form definition Meta class"""

        model = models.Image
        fields = (
            "host",
            "name",
            "version",
            "provider",
            "size",
            "tags",
        )
        labels = {
            "name": "Name",
            "host": "Host",
            "version": "Version",
            "provider": "Provider",
            "size": "Size",
        }


class ImageFilterForm(NetBoxModelFilterSetForm):
    """Image filter form definition class"""

    model = models.Image
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    version = forms.CharField(
        label="Version", max_length=256, min_length=1, required=False
    )
    provider = forms.ChoiceField(
        label="Provider",
        choices=models.ImageProviderChoices,
        required=False,
    )
    tag = TagFilterField(model)


class ImageImportForm(NetBoxModelImportForm):
    """Image importation form definition class"""

    version = forms.CharField(required=False, empty_value="latest")
    provider = forms.CharField(required=False, empty_value="dockerhub")
    size = forms.CharField(required=False, empty_value="0")

    class Meta:
        """Image importation form definition Meta class"""

        model = models.Image
        fields = ("name", "version", "provider", "size", "host")
        labels = {
            "name": "Unique Image name",
            "version": "Image version",
            "provider": 'Image provider. Can be "dockerhub" and "github"',
            "size": "Optional image size. Default 0",
            "host": "Host identifier",
        }


class ImageBulkEditForm(NetBoxModelBulkEditForm):
    """Image bulk edit form definition class"""

    version = forms.CharField(
        required=False,
    )
    provider = forms.ChoiceField(choices=models.ImageProviderChoices, required=False)
    size = forms.IntegerField(required=False)

    model = models.Image
    fieldsets = (("General", ("version", "provider", "size")),)
