# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0034_container_log_driver_alter_container_containerid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="volume",
            name="max_size",
            field=models.PositiveIntegerField(
                null=True,
                blank=True,
                default=None,
            ),
        ),
    ]
