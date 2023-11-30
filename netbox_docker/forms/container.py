"""Container Forms definitions"""

from django import forms
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
from ..models.volume import Volume
from ..models.host import Host
from ..models.container import Container, ContainerStateChoices
from ..models.image import Image
from ..models.network import Network


class ContainerForm(NetBoxModelForm):
    """Container form definition class"""

    host = DynamicModelChoiceField(
        label="Host", queryset=Host.objects.all(), required=True
    )
    image = DynamicModelChoiceField(
        label="Image",
        queryset=Image.objects.all(),
        required=True,
        query_params={"host_id": "$host"},
    )
    network = DynamicModelChoiceField(
        label="Network",
        queryset=Network.objects.all(),
        required=False,
        query_params={"host_id": "$host"},
    )

    class Meta:
        """Container form definition Meta class"""

        model = Container
        fields = (
            "host",
            "image",
            "network",
            "name",
            "tags",
        )
        labels = {
            "name": "Name",
            "host": "Host",
            "image": "Image",
            "network": "Network",
        }


class ContainerFilterForm(NetBoxModelFilterSetForm):
    """Container filter form definition class"""

    model = Volume
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    host_id = DynamicModelMultipleChoiceField(
        queryset=Host.objects.all(),
        required=False,
        label="Host",
    )
    image_id = DynamicModelMultipleChoiceField(
        queryset=Image.objects.all(),
        required=False,
        label="Image",
    )
    network_id = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Network",
    )
    state = forms.ChoiceField(
        label="State",
        choices=ContainerStateChoices,
        required=False,
    )
    tag = TagFilterField(model)


class ContainerImportForm(NetBoxModelImportForm):
    """Container importation form definition class"""

    state = forms.ChoiceField(
        label="State",
        choices=ContainerStateChoices,
        required=False,
        help_text="Container State. Can be `created`, `restarting`, " +
            "`running`, `paused`, `exited`or `dead`.",
    )

    class Meta:
        """Container importation form definition Meta class"""

        model = Container
        fields = ("name", "host", "image", "network", "state")
        labels = {
            "name": "Unique container name",
            "host": "Host identifier",
            "image": "Image identifier",
            "network": "Network identifier",
            "state": "Container State. Can be `created`, `restarting`, " +
                "`running`, `paused`, `exited`or `dead`.",
        }


class ContainerBulkEditForm(NetBoxModelBulkEditForm):
    """Container bulk edit form definition class"""

    state = forms.ChoiceField(
        label="State",
        choices=ContainerStateChoices,
        required=True,
    )

    model = Container
    fieldsets = (("General", ("state",)),)
