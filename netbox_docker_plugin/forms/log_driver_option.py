"""Log Driver option Form definition"""

from django import forms
from ..models.container import LogDriverOption, Container


class LogDriverOptionForm(forms.ModelForm):
    """Log Driver option form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
    )

    class Meta:
        """Log Driver option form definition Meta class"""

        model = LogDriverOption
        fields = (
            "container",
            "option_name",
            "value",
        )
        labels = {
            "option_name": "Option Name",
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

        self.instance._meta.verbose_name = f"Log driver option — {container.first()}"
