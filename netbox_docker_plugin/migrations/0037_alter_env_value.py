# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0036_alter_container_log_driver"),
    ]

    operations = [
        migrations.AlterField(
            model_name="env",
            name="value",
            field=models.CharField(
                blank=True,
                max_length=32768,
                validators=[
                    django.core.validators.MaxLengthValidator(limit_value=32768)
                ],
            ),
        ),
    ]
