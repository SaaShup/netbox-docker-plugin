"""Mount Form definition"""

from django import forms
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import Bind, Container


class BindForm(forms.ModelForm):
    """Bind form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
    )

    class Meta:
        """Mount form definition Meta class"""

        model = Bind
        fields = (
            "container",
            "host_path",
            "container_path",
            "read_only",
        )
        labels = {
            "container": "Container",
            "host_path": "Path to mount on host",
            "container_path": "Mountpoint in container",
            "read_only": "Mount as read-only within the container",
        }


class BindFilterForm(NetBoxModelFilterSetForm):
    """Bind filter form definition class"""

    model = Bind
    container_id = DynamicModelMultipleChoiceField(
        queryset=Container.objects.all(),
        required=False,
        label="Container",
    )
