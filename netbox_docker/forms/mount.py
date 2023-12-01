"""Mount Form definition"""

from django import forms
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.mixins import BootstrapMixin
from ..models.container import Mount, Container
from ..models.volume import Volume


class MountForm(BootstrapMixin, forms.ModelForm):
    """Mount form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
    )
    volume = DynamicModelChoiceField(
        label="Volume",
        queryset=Volume.objects.all(),
        required=True
    )

    class Meta:
        """Mount form definition Meta class"""

        model = Mount
        fields = (
            "container",
            "source",
            "volume",
        )
        labels = {
            "container": "Container",
            "source": "Source directory",
            "volume": "Volume",
        }
