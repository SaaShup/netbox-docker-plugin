"""Mount Form definition"""

from django import forms
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.mixins import BootstrapMixin
from ..models.container import Mount, Container
from ..models.volume import Volume
from ..models.host import Host


class MountForm(BootstrapMixin, forms.ModelForm):
    """Mount form definition class"""

    host = DynamicModelChoiceField(
        label="Host", queryset=Host.objects.all(), required=True
    )
    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
    )
    volume = DynamicModelChoiceField(
        label="Volume",
        queryset=Volume.objects.all(),
        required=True,
        query_params={"host_id": "$container"},
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
