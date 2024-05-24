# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0029_alter_container_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="container",
            name="ContainerID",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=128,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=128),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="container",
            name="hostname",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=256,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=256),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="Digest",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=512,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=512),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="ImageID",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=128,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=128),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="NetworkID",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=128,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=128),
                ],
            ),
        ),
    ]
