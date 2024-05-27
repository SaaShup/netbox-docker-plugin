"""NetworkSetting Form definition"""

from django import forms
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import NetworkSetting, Container
from ..models.network import Network


class NetworkSettingForm(forms.ModelForm):
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

class NetworkSettingFilterForm(NetBoxModelFilterSetForm):
    """Mount filter form definition class"""

    model = NetworkSetting
    container_id = DynamicModelMultipleChoiceField(
        queryset=Container.objects.all(),
        required=False,
        label="Container",
    )
    network_id = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Network",
    )
