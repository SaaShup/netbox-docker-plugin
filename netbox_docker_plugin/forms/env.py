"""Env Form definition"""

from django import forms
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.mixins import BootstrapMixin
from ..models.container import Env, Container


class EnvForm(BootstrapMixin, forms.ModelForm):
    """Env form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
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
            "container": "Container",
            "var_name": "Variable Name",
            "value": "Value",
        }
