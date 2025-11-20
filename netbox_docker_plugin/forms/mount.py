"""Mount Form definition"""

from django import forms
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import Mount, Container
from ..models.volume import Volume


class MountForm(forms.ModelForm):
    """Mount form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
    )
    volume = forms.ModelChoiceField(
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
            "source": "Source directory",
            "volume": "Volume",
            "read_only": "Mount as read-only within the container",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "data" in kwargs:
            container = Container.objects.filter(id=kwargs["data"]["container"])
        elif "initial" in kwargs and "container" in kwargs["initial"]:
            container = Container.objects.filter(id=kwargs["initial"]["container"])
        else:
            container = Container.objects.filter(id=self.instance.container.id)

        self.fields["volume"].queryset = Volume.objects.filter(
            host=container.first().host
        )

        self.instance._meta.verbose_name = f"Mount — {container.first()}"


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
