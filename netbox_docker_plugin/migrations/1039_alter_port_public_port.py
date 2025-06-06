# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0038_container_cmd"),
    ]

    operations = [
        migrations.AlterField(
            model_name="port",
            name="public_port",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(limit_value=-1),
                    django.core.validators.MaxValueValidator(limit_value=65535),
                ]
            ),
        ),
    ]
