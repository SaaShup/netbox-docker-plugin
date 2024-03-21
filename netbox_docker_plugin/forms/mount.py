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
        max_length=1024,
        required=False,
    )

    def clean_host_path(self):
        """Clean host path form field"""
        host_path = self.cleaned_data["host_path"]

        if host_path and not host_path.startswith("/"):
            raise forms.ValidationError("Host path must be an absolute path")

        return host_path

    def clean(self):
        """Clean form fields"""
        cleaned_data = super().clean()
        volume = cleaned_data.get("volume")
        host_path = cleaned_data.get("host_path")

        if not volume and not host_path:
            raise forms.ValidationError("Either volume or host path must be set.")

        return cleaned_data

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
