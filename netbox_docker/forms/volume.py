"""Volume Forms definitions"""

from django import forms
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)
from ..models.volume import Volume, VolumeDriverChoices
from ..models.host import Host


class VolumeForm(NetBoxModelForm):
    """Volume form definition class"""

    class Meta:
        """Volume form definition Meta class"""

        model = Volume
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


class VolumeFilterForm(NetBoxModelFilterSetForm):
    """Volume filter form definition class"""

    model = Volume
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    driver = forms.ChoiceField(
        label="Driver",
        choices=VolumeDriverChoices,
        required=False,
    )
    host_id = DynamicModelMultipleChoiceField(
        queryset=Host.objects.all(),
        required=False,
        label="Host",
    )
    tag = TagFilterField(model)


class VolumeImportForm(NetBoxModelImportForm):
    """Volume importation form definition class"""

    driver = forms.CharField(required=False, empty_value="local")

    class Meta:
        """Volume importation form definition Meta class"""

        model = Volume
        fields = ("name", "driver", "host")
        labels = {
            "name": "Unique Image name",
            "driver": 'Volume provider. Can be "local"',
            "host": "Host identifier",
        }
