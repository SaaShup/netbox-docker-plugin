# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0025_alter_image_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="Digest",
            field=models.CharField(
                blank=True,
                max_length=512,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=512),
                ],
            ),
        ),
    ]
