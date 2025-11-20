"""Label Form definition"""

from django import forms
from ..models.container import Label, Container


class LabelForm(forms.ModelForm):
    """Label form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
    )

    class Meta:
        """Label form definition Meta class"""

        model = Label
        fields = (
            "container",
            "key",
            "value",
        )
        labels = {
            "key": "Key",
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

        self.instance._meta.verbose_name = f"Label — {container.first()}"
