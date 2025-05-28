# pylint: disable=C0103
"""Migration file"""

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0037_alter_env_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="cmd",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=1024, null=True),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]
