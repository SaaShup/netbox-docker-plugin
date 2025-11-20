"""NetworkSetting Form definition"""

from django import forms
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
from netbox.forms import (
    NetBoxModelFilterSetForm,
)
from ..models.container import NetworkSetting, Container
from ..models.network import Network


class NetworkSettingForm(forms.ModelForm):
    """NetworkSetting form definition class"""

    container = forms.ModelChoiceField(
        label="Container",
        queryset=Container.objects.all(),
        required=True,
        widget=forms.HiddenInput,
    )
    network = forms.ModelChoiceField(
        label="Network", queryset=Network.objects.all(), required=True
    )

    class Meta:
        """NetworkSetting form definition Meta class"""

        model = NetworkSetting
        fields = ("container", "network")
        labels = {
            "network": "Network",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "data" in kwargs:
            container = Container.objects.filter(id=kwargs["data"]["container"])
        elif "initial" in kwargs and "container" in kwargs["initial"]:
            container = Container.objects.filter(id=kwargs["initial"]["container"])
        else:
            container = Container.objects.filter(id=self.instance.container.id)

        self.fields["network"].queryset = Network.objects.filter(
            host=container.first().host
        )

        self.instance._meta.verbose_name = f"Network setting — {container.first()}"


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
