# pylint: disable=C0103
"""Migration file: registries are no longer bound to a host"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "1046_merge_registries"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="registry",
            name="host",
        ),
        migrations.AlterField(
            model_name="registry",
            name="name",
            field=models.CharField(
                max_length=255,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=255),
                ],
            ),
        ),
    ]
