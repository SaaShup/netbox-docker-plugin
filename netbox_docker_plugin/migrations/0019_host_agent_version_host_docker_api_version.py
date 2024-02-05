# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "0018_alter_mount_volume_alter_networksetting_network",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="host",
            name="agent_version",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="host",
            name="docker_api_version",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
