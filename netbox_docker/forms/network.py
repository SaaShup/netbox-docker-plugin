"""Network Forms definitions"""

from django import forms
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
)
from .. import models


class NetworkForm(NetBoxModelForm):
    """Network form definition class"""

    class Meta:
        """Network form definition Meta class"""

        model = models.Network
        fields = (
            "host",
            "name",
            "driver",
            "tags",
        )
        labels = {
            "name": "Name",
            "host": "Host",
            "driver": "Driver",
        }


class NetworkFilterForm(NetBoxModelFilterSetForm):
    """Network filter form definition class"""

    model = models.Network
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    driver = forms.ChoiceField(
        label="Driver",
        choices=models.NetworkDriverChoices,
        required=False,
    )
    host_id = DynamicModelMultipleChoiceField(
        queryset=models.Host.objects.all(),
        required=False,
        label="Host",
    )
    tag = TagFilterField(model)


class NetworkImportForm(NetBoxModelImportForm):
    """Network importation form definition class"""

    driver = forms.CharField(required=False, empty_value="bridge")

    class Meta:
        """Network importation form definition Meta class"""

        model = models.Network
        fields = ("name", "driver", "host")
        labels = {
            "name": "Unique Network name",
            "driver": 'Network driver. Can be "bridge", "host" or "null"',
            "host": "Host identifier",
        }


class NetworkBulkEditForm(NetBoxModelBulkEditForm):
    """Network bulk edit form definition class"""

    driver = forms.ChoiceField(choices=models.NetworkDriverChoices, required=False)

    model = models.Network
    fieldsets = (
        (
            "General",
            ("driver",),
        ),
    )
