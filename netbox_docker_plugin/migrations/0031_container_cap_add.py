# pylint: disable=C0103
"""Migration file"""

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "0030_alter_container_containerid_alter_container_hostname_and_more",
        ),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE netbox_docker_plugin_container "
            + "ADD COLUMN IF NOT EXISTS cap_add character varying(32)[];",
            state_operations=[
                migrations.AddField(
                    model_name="container",
                    name="cap_add",
                    field=django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True, max_length=32, null=True
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
            ],
        )
    ]
