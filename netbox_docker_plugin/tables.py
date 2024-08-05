"""Tables definitions"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models.host import Host
from .models.image import Image
from .models.volume import Volume
from .models.network import Network
from .models.container import (
    Container,
    Env,
    Label,
    Port,
    Mount,
    Bind,
    NetworkSetting,
    Device,
)
from .models.registry import Registry
from .templatetags.host import remove_password


class HostTable(NetBoxTable):
    """Host Table definition class"""

    name = tables.Column(linkify=True)
    image_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:image_list",
        url_params={"host_id": "pk"},
        verbose_name="Images count",
    )
    volume_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:volume_list",
        url_params={"host_id": "pk"},
        verbose_name="Volumes count",
    )
    network_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:network_list",
        url_params={"host_id": "pk"},
        verbose_name="Networks count",
    )
    container_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:container_list",
        url_params={"host_id": "pk"},
        verbose_name="Containers count",
    )
    tags = columns.TagColumn()

    def render_endpoint(self, value):
        """Render endpoint without password"""
        return remove_password(value)

    class Meta(NetBoxTable.Meta):
        """Host Table definition Meta class"""

        model = Host
        fields = (
            "pk",
            "id",
            "name",
            "endpoint",
            "state",
            "agent_version",
            "docker_api_version",
            "image_count",
            "volume_count",
            "network_count",
            "container_count",
            "tags",
        )
        default_columns = (
            "name",
            "endpoint",
            "state",
            "image_count",
            "volume_count",
            "network_count",
            "container_count",
        )


class RegistryTable(NetBoxTable):
    """Registry Table definition class"""

    name = tables.Column(linkify=True)
    image_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:image_list",
        url_params={"registry_id": "pk"},
        verbose_name="Images count",
    )
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Registry Table definition Meta class"""

        model = Registry
        fields = (
            "pk",
            "id",
            "name",
            "serveraddress",
            "username",
            "email",
            "image_count",
            "tags",
        )
        default_columns = (
            "name",
            "serveraddress",
            "image_count",
        )


class ImageTable(NetBoxTable):
    """Image Table definition class"""

    host = tables.Column(linkify=True)
    registry = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    container_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:container_list",
        url_params={"image_id": "pk"},
        verbose_name="Used by (containers)",
    )
    tags = columns.TagColumn()

    def render_size(self, value):
        """Render the image size with unity"""
        return f"{value} MB"

    class Meta(NetBoxTable.Meta):
        """Image Table definition Meta class"""

        model = Image
        fields = (
            "pk",
            "id",
            "host",
            "name",
            "version",
            "registry",
            "size",
            "ImageID",
            "container_count",
            "tags",
        )
        default_columns = (
            "name",
            "version",
            "registry",
            "size",
            "host",
            "container_count",
        )


class VolumeTable(NetBoxTable):
    """Volume Table definition class"""

    host = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    mount_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:mount_list",
        url_params={"volume_id": "pk"},
        verbose_name="Used by (mounts)",
    )
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Volume Table definition Meta class"""

        model = Volume
        fields = ("pk", "id", "host", "name", "driver", "mount_count", "tags")
        default_columns = ("name", "driver", "host", "mount_count")


class NetworkTable(NetBoxTable):
    """Network Table definition class"""

    host = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    networksetting_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:networksetting_list",
        url_params={"network_id": "pk"},
        verbose_name="Used by (network settings)",
    )
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Network Table definition Meta class"""

        model = Network
        fields = (
            "pk",
            "id",
            "host",
            "name",
            "driver",
            "NetworkID",
            "state",
            "networksetting_count",
            "tags",
        )
        default_columns = ("name", "driver", "state", "host", "networksetting_count")


class ContainerTable(NetBoxTable):
    """Network Table definition class"""

    host = tables.Column(linkify=True)
    image = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    port_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:port_list",
        url_params={"container_id": "pk"},
        verbose_name="Ports count",
    )
    mount_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:mount_list",
        url_params={"container_id": "pk"},
        verbose_name="Mounts count",
    )
    bind_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:bind_list",
        url_params={"container_id": "pk"},
        verbose_name="Binds count",
    )
    networksetting_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:networksetting_list",
        url_params={"container_id": "pk"},
        verbose_name="Network Settings count",
    )
    env_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:env_list",
        url_params={"container_id": "pk"},
        verbose_name="Env variables count",
    )
    label_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:label_list",
        url_params={"container_id": "pk"},
        verbose_name="Labels count",
    )
    device_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker_plugin:device_list",
        url_params={"container_id": "pk"},
        verbose_name="Devices count",
    )
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Container Table definition Meta class"""

        model = Container
        fields = (
            "pk",
            "id",
            "host",
            "name",
            "image",
            "state",
            "status",
            "ContainerID",
            "hostname",
            "restart_policy",
            "cap_add",
            "port_count",
            "mount_count",
            "bind_count",
            "networksetting_count",
            "env_count",
            "label_count",
            "device_count",
            "tags",
        )
        default_columns = (
            "name",
            "host",
            "image",
            "state",
            "port_count",
            "mount_count",
            "bind_count",
            "networksetting_count",
            "env_count",
            "label_count",
        )


class EnvTable(NetBoxTable):
    """Env Table definition class"""

    container = tables.Column(linkify=True)

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Env Table definition Meta class"""

        model = Env
        fields = ("container", "var_name", "value")
        default_columns = ("container", "var_name", "value")


class LabelTable(NetBoxTable):
    """Label Table definition class"""

    container = tables.Column(linkify=True)

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Label Table definition Meta class"""

        model = Label
        fields = ("container", "key", "value")
        default_columns = ("container", "key", "value")


class PortTable(NetBoxTable):
    """Port Table definition class"""

    container = tables.Column(linkify=True)

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Port Table definition Meta class"""

        model = Port
        fields = ("container", "public_port", "private_port", "type")
        default_columns = ("container", "public_port", "private_port", "type")


class MountTable(NetBoxTable):
    """Mount Table definition class"""

    container = tables.Column(linkify=True)
    volume = tables.Column(linkify=True)

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Mount Table definition Meta class"""

        model = Mount
        fields = (
            "container",
            "source",
            "volume",
            "read_only",
        )
        default_columns = (
            "container",
            "source",
            "volume",
            "read_only",
        )


class BindTable(NetBoxTable):
    """Bind Table definition class"""

    container = tables.Column(linkify=True)

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Bind Table definition Meta class"""

        model = Bind
        fields = (
            "container",
            "host_path",
            "container_path",
            "read_only",
        )
        default_columns = (
            "container",
            "host_path",
            "container_path",
            "read_only",
        )


class NetworkSettingTable(NetBoxTable):
    """NetworkSetting Table definition class"""

    container = tables.Column(linkify=True)
    network = tables.Column(linkify=True)

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """NetworkSetting Table definition Meta class"""

        model = NetworkSetting
        fields = (
            "container",
            "network",
        )
        default_columns = (
            "container",
            "network",
        )


class DeviceTable(NetBoxTable):
    """Device Table definition class"""

    container = tables.Column(linkify=True)

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Device Table definition Meta class"""

        model = Device
        fields = (
            "container",
            "host_path",
            "container_path",
        )
        default_columns = (
            "container",
            "host_path",
            "container_path",
        )
