"""Mount Form definition"""

from django import forms
from utilities.forms.mixins import BootstrapMixin
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import Mount, Container
from ..models.volume import Volume


class MountForm(BootstrapMixin, forms.ModelForm):
    """Mount form definition class"""

    container = DynamicModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
    )
    volume = DynamicModelChoiceField(
        label="Volume",
        queryset=Volume.objects.all(),
        required=False,
    )
    host_path = forms.CharField(
        label="Host path",
        min_length=1,
        max_length=1024,
        required=False,
    )

    class Meta:
        """Mount form definition Meta class"""

        model = Mount
        fields = (
            "container",
            "source",
            "volume",
            "host_path",
        )
        labels = {
            "container": "Container",
            "source": "Source directory",
            "volume": "Volume",
            "host_path": "Host path",
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
