"""Network Forms definitions"""

from django import forms
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField
from utilities.choices import ChoiceSet
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
)
from ..models.network import Network, NetworkDriverChoices, NetworkStateChoices
from ..models.host import Host


class FormNetworkDriverChoices(ChoiceSet):
    """Network driver choices definition class"""

    key = "Network.driver"

    DEFAULT_VALUE = "bridge"

    CHOICES = [
        ("bridge", "Bridge", "blue"),
        ("host", "Host", "red"),
    ]


class NetworkForm(NetBoxModelForm):
    """Network form definition class"""

    driver = forms.ChoiceField(
        label="Driver",
        choices=FormNetworkDriverChoices,
        required=False,
    )

    class Meta:
        """Network form definition Meta class"""

        model = Network
        fields = (
            "host",
            "name",
            "driver",
            "NetworkID",
            "tags",
        )
        labels = {
            "name": "Name",
            "host": "Host",
            "driver": "Driver",
        }


class NetworkFilterForm(NetBoxModelFilterSetForm):
    """Network filter form definition class"""

    model = Network
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    driver = forms.ChoiceField(
        label="Driver",
        choices=NetworkDriverChoices,
        required=False,
    )
    host_id = DynamicModelMultipleChoiceField(
        queryset=Host.objects.all(),
        required=False,
        label="Host",
    )
    NetworkID = forms.CharField(
        label="NetworkID", max_length=128, min_length=1, required=False
    )
    state = forms.ChoiceField(
        label="Driver",
        choices=NetworkStateChoices,
        required=False,
    )
    tag = TagFilterField(model)


class NetworkImportForm(NetBoxModelImportForm):
    """Network importation form definition class"""

    driver = forms.CharField(required=False, empty_value="bridge")

    class Meta:
        """Network importation form definition Meta class"""

        model = Network
        fields = ("name", "driver", "host")
        labels = {
            "name": "Unique Network name",
            "driver": 'Network driver. Can be "bridge", "host" or "null"',
            "host": "Host identifier",
        }


class NetworkBulkEditForm(NetBoxModelBulkEditForm):
    """Network bulk edit form definition class"""

    driver = forms.ChoiceField(choices=NetworkDriverChoices, required=False)
    NetworkID = forms.CharField(required=False, label="NetworkID")

    model = Network
    fieldsets =(FieldSet("driver", "NetworkID", name="General"),)
