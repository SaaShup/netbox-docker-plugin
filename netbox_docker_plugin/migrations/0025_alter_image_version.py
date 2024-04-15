# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0024_registry_host_alter_registry_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="version",
            field=models.CharField(
                default="latest",
                max_length=256,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=256),
                ],
            ),
        ),
    ]
