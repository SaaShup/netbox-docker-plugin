"""Device Form definition"""

from django import forms
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import Device, Container


class DeviceForm(forms.ModelForm):
    """Device form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
    )

    class Meta:
        """Device form definition Meta class"""

        model = Device
        fields = (
            "container",
            "host_path",
            "container_path",
        )
        labels = {
            "container": "Container",
            "host_path": "Path to the device on host",
            "container_path": "Path to the device in container",
        }


class DeviceFilterForm(NetBoxModelFilterSetForm):
    """Device filter form definition class"""

    model = Device
    container_id = DynamicModelMultipleChoiceField(
        queryset=Container.objects.all(),
        required=False,
        label="Container",
    )
