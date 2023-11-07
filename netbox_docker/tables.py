"""Tables definitions"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from . import models


class HostTable(NetBoxTable):
    """Host Table definition class"""

    name = tables.Column(linkify=True)
    image_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker:image_list",
        url_params={"host_id": "pk"},
        verbose_name="Images count",
    )
    volume_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker:volume_list",
        url_params={"host_id": "pk"},
        verbose_name="Volumes count",
    )
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Host Table definition Meta class"""

        model = models.Host
        fields = ("pk", "id", "name", "endpoint", "image_count", "tags")
        default_columns = ("name", "endpoint", "image_count", "volume_count")


class ImageTable(NetBoxTable):
    """Image Table definition class"""

    host = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Image Table definition Meta class"""

        model = models.Image
        fields = ("pk", "id", "host", "name", "version", "provider", "size", "tags")
        default_columns = ("name", "version", "provider", "size", "host")


class VolumeTable(NetBoxTable):
    """Volume Table definition class"""

    host = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """Volume Table definition Meta class"""

        model = models.Volume
        fields = ("pk", "id", "host", "name", "driver", "tags")
        default_columns = ("name", "driver", "host")
