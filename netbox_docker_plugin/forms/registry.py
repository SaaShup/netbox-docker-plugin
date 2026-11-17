"""Registry Forms definitions"""

from django import forms
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelFilterSetForm,
)
from ..models.registry import Registry
from ..models.host import Host


class RegistryForm(NetBoxModelForm):
    """Registry form definition class"""

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=True),
        required=False,
        empty_value=None,
    )

    class Meta:
        """Registry form definition Meta class"""

        model = Registry
        fields = (
            "name",
            "serveraddress",
            "username",
            "password",
            "email",
            "tags",
        )
        help_texts = {"name": "Unique Name", "serveraddress": "Registry URL"}
        labels = {"name": "Name", "serveraddress": "Server Address"}


class RegistryFilterForm(NetBoxModelFilterSetForm):
    """Registry filter form definition class"""

    model = Registry
    used_by_host_id = DynamicModelMultipleChoiceField(
        queryset=Host.objects.all(),
        required=False,
        label="Used by Host",
    )
    name = forms.CharField(label="Name", required=False)
    tag = TagFilterField(model)
