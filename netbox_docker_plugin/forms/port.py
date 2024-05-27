"""Port Form definition"""

from django import forms
from utilities.forms.fields import DynamicModelChoiceField
from ..models.container import Port, Container


class PortForm(forms.ModelForm):
    """Port form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
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
            "container": "Container",
            "public_port": "Public Port",
            "private_port": "Private Port",
            "type": "Type",
        }
