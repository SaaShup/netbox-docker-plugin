"""Mount Form definition"""

from django import forms
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import Bind, Container


class BindForm(forms.ModelForm):
    """Bind form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
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
            "host_path": "Path to mount on host",
            "container_path": "Mountpoint in container",
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

        self.instance._meta.verbose_name = f"Bind — {container.first()}"


class BindFilterForm(NetBoxModelFilterSetForm):
    """Bind filter form definition class"""

    model = Bind
    container_id = DynamicModelMultipleChoiceField(
        queryset=Container.objects.all(),
        required=False,
        label="Container",
    )
