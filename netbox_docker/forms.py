"""Forms definitions"""

from django import forms
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)
from utilities.forms.fields import TagFilterField
from netbox_docker import models


class HostForm(NetBoxModelForm):
    """Host form definition class"""

    class Meta:
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
    cn = forms.CharField(
        label="Name", max_length=256, min_length=1, required=False
    )
    endpoint = forms.CharField(
        label="Endpoint", max_length=256, min_length=1, required=False
    )
    tag = TagFilterField(model)


class HostImportForm(NetBoxModelImportForm):
    """Host importation form definition class"""

    class Meta:
        model = models.Host
        fields = (
            "name",
            "endpoint",
        )
        labels = {
            "name": "Unique name",
            "endpoint": "Docker instance URL",
        }
