# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("netbox_docker_plugin", "0014_container_operation"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="mount",
            name="netbox_docker_plugin_mount_unique_volume",
        ),
        migrations.AddConstraint(
            model_name="mount",
            constraint=models.UniqueConstraint(
                fields=("container", "source", "volume"),
                name="netbox_docker_plugin_mount_unique_volume",
            ),
        ),
    ]
