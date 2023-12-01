"""NetworkSetting Form definition"""

from django import forms
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.mixins import BootstrapMixin
from ..models.container import NetworkSetting, Container
from ..models.network import Network


class NetworkSettingForm(BootstrapMixin, forms.ModelForm):
    """NetworkSetting form definition class"""

    container = DynamicModelChoiceField(
        label="Container", queryset=Container.objects.all(), required=True
    )
    network = DynamicModelChoiceField(
        label="Network", queryset=Network.objects.all(), required=True
    )

    class Meta:
        """NetworkSetting form definition Meta class"""

        model = NetworkSetting
        fields = (
            "container",
            "network"
        )
        labels = {
            "container": "Container",
            "network": "Network",
        }
