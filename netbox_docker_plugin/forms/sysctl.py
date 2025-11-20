"""Sysctl Form definition"""

from django import forms
from ..models.container import Sysctl, Container


class SysctlForm(forms.ModelForm):
    """Sysctl form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
    )

    class Meta:
        """Sysctl form definition Meta class"""

        model = Sysctl
        fields = (
            "container",
            "key",
            "value",
        )
        labels = {
            "key": " Sysctl Key",
            "value": "Value",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "data" in kwargs:
            container = Container.objects.filter(id=kwargs["data"]["container"])
        elif "initial" in kwargs and "container" in kwargs["initial"]:
            container = Container.objects.filter(id=kwargs["initial"]["container"])
        else:
            container = Container.objects.filter(id=self.instance.container.id)

        self.instance._meta.verbose_name = f"Sysctl — {container.first()}"
