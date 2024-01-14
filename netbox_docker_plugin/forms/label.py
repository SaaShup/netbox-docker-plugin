"""Label Form definition"""

from django import forms
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.mixins import BootstrapMixin
from ..models.container import Label, Container


class LabelForm(BootstrapMixin, forms.ModelForm):
    """Label form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
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
            "container": "Container",
            "key": "Key",
            "value": "Value",
        }
