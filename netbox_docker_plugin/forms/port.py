"""Port Form definition"""

from django import forms
from ..models.container import Port, Container


class PortForm(forms.ModelForm):
    """Port form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
    )

    class Meta:
        """Port form definition Meta class"""

        model = Port
        fields = (
            "container",
            "public_port",
            "private_port",
            "type",
        )
        labels = {
            "public_port": "Public Port",
            "private_port": "Private Port",
            "type": "Type",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "data" in kwargs:
            container = Container.objects.filter(id=kwargs["data"]["container"])
        elif "initial" in kwargs and "container" in kwargs["initial"]:
            container = Container.objects.filter(id=kwargs["initial"]["container"])
        else:
            container = Container.objects.filter(id=self.instance.container.id)

        self.instance._meta.verbose_name = f"Port mapping — {container.first()}"
