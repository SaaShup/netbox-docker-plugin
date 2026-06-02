"""Host Forms definitions"""

from django import forms
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import TagFilterField, DynamicModelChoiceField
from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
)
from virtualization.models import VirtualMachine
from ..models.host import Host, HostStateChoices


class HostAddForm(NetBoxModelForm):
    """Host form definition class"""

    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        selector=True,
        required=False,
        label="Virtual Machine",
    )

    class Meta:
        """Host form definition Meta class"""

        model = Host
        fields = (
            "name",
            "endpoint",
            "virtual_machine",
        )
        help_texts = {"name": "Unique Name", "endpoint": "Docker instance endpoint"}
        labels = {"name": "Name", "endpoint": "Endpoint"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("tags", None)


class HostForm(NetBoxModelForm):
    """Host form definition class"""

    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        selector=True,
        required=False,
        label="Virtual Machine",
    )

    class Meta:
        """Host form definition Meta class"""

        model = Host
        fields = (
            "name",
            "endpoint",
            "virtual_machine",
            "tags",
        )
        help_texts = {"name": "Unique Name", "endpoint": "Docker instance endpoint"}
        labels = {"name": "Name", "endpoint": "Endpoint"}


class HostFilterForm(NetBoxModelFilterSetForm):
    """Host filter form definition class"""

    model = Host
    name = forms.CharField(label="Name", max_length=256, min_length=1, required=False)
    endpoint = forms.CharField(
        label="Endpoint", max_length=256, min_length=1, required=False
    )
    state = forms.ChoiceField(label="State", choices=HostStateChoices, required=False)
    agent_version = forms.CharField(
        label="Agent Version", max_length=32, min_length=1, required=False
    )
    docker_api_version = forms.CharField(
        label="Docker API Version", max_length=32, min_length=1, required=False
    )
    tag = TagFilterField(model)


class HostImportForm(NetBoxModelImportForm):
    """Host importation form definition class"""

    class Meta:
        """Host importation form definition Meta class"""

        model = Host
        fields = (
            "name",
            "endpoint",
        )
        labels = {
            "name": "Unique name",
            "endpoint": "Docker instance URL",
        }


class HostBulkEditForm(NetBoxModelBulkEditForm):
    """Host bulk edit form definition class"""

    endpoint = forms.CharField(
        required=False,
    )

    model = Host
    fieldsets = (FieldSet("endpoint", name="General"),)


class HostOperationForm(NetBoxModelForm):
    """Host Operation form definition class"""

    class Meta:
        """Host form definition Meta class"""

        model = Host
        fields = ("operation",)
