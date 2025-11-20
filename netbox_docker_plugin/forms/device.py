"""Device Form definition"""

from django import forms
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import Device, Container


class DeviceForm(forms.ModelForm):
    """Device form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
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
            "host_path": "Path to the device on host",
            "container_path": "Path to the device in container",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "data" in kwargs:
            container = Container.objects.filter(id=kwargs["data"]["container"])
        elif "initial" in kwargs and "container" in kwargs["initial"]:
            container = Container.objects.filter(id=kwargs["initial"]["container"])
        else:
            container = Container.objects.filter(id=self.instance.container.id)

        self.instance._meta.verbose_name = f"Device — {container.first()}"


class DeviceFilterForm(NetBoxModelFilterSetForm):
    """Device filter form definition class"""

    model = Device
    container_id = DynamicModelMultipleChoiceField(
        queryset=Container.objects.all(),
        required=False,
        label="Container",
    )
