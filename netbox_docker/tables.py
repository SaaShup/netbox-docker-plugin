"""Tables definitions"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from netbox_docker import models

class HostTable(NetBoxTable):
    """Host Table definition class"""

    name = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = models.Host
        fields = (
            "pk",
            "id",
            "name",
            "endpoint",
            "tags"
        )
        default_columns = (
            "name",
            "endpoint"
        )
