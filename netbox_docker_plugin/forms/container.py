"""Container Forms definitions"""

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
from ..models.volume import Volume
from ..models.host import Host
from ..models.container import (
    Container,
    ContainerRestartPolicyChoices,
    ContainerCapAddChoices,
)
from ..models.image import Image


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
    cap_add = forms.MultipleChoiceField(choices=ContainerCapAddChoices, required=False)

    class Meta:
        """Container form definition Meta class"""

        model = Container
        fields = (
            "host",
            "image",
            "name",
            "hostname",
            "restart_policy",
            "cap_add",
            "log_driver",
            "cmd",
            "tags",
        )
        labels = {
            "name": "Name",
            "host": "Host",
            "image": "Image",
            "hostname": "Hostname",
            "restart_policy": "Restart Policy",
            "cap_add": "Add Host capabilities",
            "log_driver": "Logging driver",
            "cmd": "Command",
        }


class ContainerEditForm(NetBoxModelForm):
    """Container form definition class"""

    image = DynamicModelChoiceField(
        label="Image",
        queryset=Image.objects.all(),
        required=True,
        query_params={"host_id": "$host"},
    )
    cap_add = forms.MultipleChoiceField(choices=ContainerCapAddChoices, required=False)

    class Meta:
        """Container form definition Meta class"""

        model = Container
        fields = (
            "image",
            "name",
            "hostname",
            "restart_policy",
            "cap_add",
            "log_driver",
            "cmd",
            "tags",
        )
        labels = {
            "name": "Name",
            "image": "Image",
            "hostname": "Hostname",
            "restart_policy": "Restart Policy",
            "cap_add": "Add Host capabilities",
            "log_driver": "Logging driver",
            "cmd": "Command",
        }


class ContainerFilterForm(NetBoxModelFilterSetForm):
    """Container filter form definition class"""

    model = Volume
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    ContainerID = forms.CharField(
        label="Name", max_length=128, min_length=1, required=False
    )
    hostname = forms.CharField(
        label="Hostname", max_length=256, min_length=1, required=False
    )
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
    restart_policy = forms.ChoiceField(
        label="Restart Policy", choices=ContainerRestartPolicyChoices, required=False
    )
    log_driver = forms.ChoiceField(
        label="Logging driver", required=False
    )
    tag = TagFilterField(model)


class ContainerImportForm(NetBoxModelImportForm):
    """Container importation form definition class"""

    restart_policy = forms.ChoiceField(
        label="Restart Policy",
        choices=ContainerRestartPolicyChoices,
        required=False,
        help_text="Container restart policy. Can be `no`, `on-failure`, "
        + "`always`, `unless-stopped`.",
    )

    log_driver = forms.CharField(
        label="Logging driver",
        required=False,
        help_text="Logging driver. Can be `json-file`, `syslog`.",
    )

    class Meta:
        """Container importation form definition Meta class"""

        model = Container
        fields = (
            "name",
            "host",
            "image",
            "hostname",
        )
        labels = {
            "name": "Unique container name",
            "host": "Host identifier",
            "image": "Image identifier",
        }


class ContainerBulkEditForm(NetBoxModelBulkEditForm):
    """Container bulk edit form definition class"""

    restart_policy = forms.ChoiceField(
        label="Restart Policy",
        choices=ContainerRestartPolicyChoices,
        required=True,
    )
    log_driver = forms.CharField(
        label="Logging driver",
        required=False,
    )
    hostname = forms.CharField(
        label="Hostname", max_length=256, min_length=1, required=False
    )

    model = Container
    fieldsets = (FieldSet("restart_policy", "log_driver", "hostname", name="General"),)


class ContainerOperationForm(NetBoxModelForm):
    """Container Operation form definition class"""

    class Meta:
        """Container form definition Meta class"""

        model = Container
        fields = ("operation",)
