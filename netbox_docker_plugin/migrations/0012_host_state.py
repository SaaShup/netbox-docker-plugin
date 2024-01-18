# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models
from netbox_docker_plugin.models.host import HostStateChoices


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("netbox_docker_plugin", "0011_host_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="host",
            name="state",
            field=models.CharField(
                default=HostStateChoices.STATE_CREATED, max_length=32
            ),
        ),
    ]
