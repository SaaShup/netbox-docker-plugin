# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0032_device_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE netbox_docker_plugin_host "
            + "ADD COLUMN IF NOT EXISTS operation character varying(32);",
            state_operations=[
                migrations.AddField(
                    model_name="host",
                    name="operation",
                    field=models.CharField(default="none", max_length=32),
                ),
            ],
        )
    ]
