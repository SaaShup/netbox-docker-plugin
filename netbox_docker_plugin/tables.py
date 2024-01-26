"""Tables definitions"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models.host import Host
from .models.image import Image
from .models.volume import Volume
from .models.network import Network
from .models.container import Container, Env, Label, Port, Mount, NetworkSetting


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

    class Meta(NetBoxTable.Meta):
        """Host Table definition Meta class"""

        model = Host
        fields = (
            "pk",
            "id",
            "name",
            "endpoint",
            "state",
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


class ImageTable(NetBoxTable):
    """Image Table definition class"""

    host = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Image Table definition Meta class"""

        model = Image
        fields = (
            "pk",
            "id",
            "host",
            "name",
            "version",
            "provider",
            "size",
            "ImageID",
            "tags",
        )
        default_columns = ("name", "version", "provider", "size", "host")


class VolumeTable(NetBoxTable):
    """Volume Table definition class"""

    host = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Volume Table definition Meta class"""

        model = Volume
        fields = ("pk", "id", "host", "name", "driver", "tags")
        default_columns = ("name", "driver", "host")


class NetworkTable(NetBoxTable):
    """Network Table definition class"""

    host = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Network Table definition Meta class"""

        model = Network
        fields = ("pk", "id", "host", "name", "driver", "NetworkID", "state", "tags")
        default_columns = ("name", "driver", "state", "host")


class ContainerTable(NetBoxTable):
    """Network Table definition class"""

    host = tables.Column(linkify=True)
    image = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
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
            "tags",
        )
        default_columns = ("name", "host", "image", "state")


class EnvTable(NetBoxTable):
    """Env Table definition class"""

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Env Table definition Meta class"""

        model = Env
        fields = ("var_name", "value")
        default_columns = ("var_name", "value")


class LabelTable(NetBoxTable):
    """Label Table definition class"""

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Label Table definition Meta class"""

        model = Label
        fields = ("key", "value")
        default_columns = ("key", "value")


class PortTable(NetBoxTable):
    """Port Table definition class"""

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Port Table definition Meta class"""

        model = Port
        fields = ("public_port", "private_port", "type")
        default_columns = ("public_port", "private_port", "type")


class MountTable(NetBoxTable):
    """Mount Table definition class"""

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """Mount Table definition Meta class"""

        model = Mount
        fields = ("source", "volume")
        default_columns = ("source", "volume")


class NetworkSettingTable(NetBoxTable):
    """NetworkSetting Table definition class"""

    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        """NetworkSetting Table definition Meta class"""

        model = NetworkSetting
        fields = ("network",)
        default_columns = ("network",)
