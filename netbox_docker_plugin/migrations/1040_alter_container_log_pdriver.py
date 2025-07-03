# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "1039_container_cmd"),
    ]

    operations = [
        migrations.AlterField(
            model_name="container",
            name="log_driver",
            field=models.CharField( max_length=32, null=True, blank=True),
        ),
    ]