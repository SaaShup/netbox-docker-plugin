# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("netbox_docker_plugin", "0002_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="size",
            field=models.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(limit_value=0),
                    django.core.validators.MaxValueValidator(limit_value=4096),
                ],
            ),
        ),
    ]
