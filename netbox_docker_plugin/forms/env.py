"""Env Form definition"""

from django import forms
from ..models.container import Env, Container


class EnvForm(forms.ModelForm):
    """Env form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
    )

    class Meta:
        """Env form definition Meta class"""

        model = Env
        fields = (
            "container",
            "var_name",
            "value",
        )
        labels = {
            "var_name": "Variable Name",
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

        self.instance._meta.verbose_name = f"Environment variable — {container.first()}"
