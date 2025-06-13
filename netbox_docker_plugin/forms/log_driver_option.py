"""Log Driver option Form definition"""

from django import forms
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.mixins import BootstrapMixin
from ..models.container import LogDriverOption, Container


class LogDriverOptionForm(BootstrapMixin, forms.ModelForm):
    """Log Driver option form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
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
            "container": "Container",
            "option_name": "Option Name",
            "value": "Value",
        }
