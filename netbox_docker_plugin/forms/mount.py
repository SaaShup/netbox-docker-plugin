"""Mount Form definition"""

from django import forms
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import Mount, Container
from ..models.volume import Volume


class MountForm(forms.ModelForm):
    """Mount form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
    )
    volume = DynamicModelChoiceField(
        label="Volume", queryset=Volume.objects.all(), required=True
    )

    class Meta:
        """Mount form definition Meta class"""

        model = Mount
        fields = (
            "container",
            "source",
            "volume",
            "read_only",
        )
        labels = {
            "container": "Container",
            "source": "Source directory",
            "volume": "Volume",
            "read_only": "Mount as read-only within the container",
        }


class MountFilterForm(NetBoxModelFilterSetForm):
    """Mount filter form definition class"""

    model = Mount
    container_id = DynamicModelMultipleChoiceField(
        queryset=Container.objects.all(),
        required=False,
        label="Container",
    )
    volume_id = DynamicModelMultipleChoiceField(
        queryset=Volume.objects.all(),
        required=False,
        label="Volume",
    )
