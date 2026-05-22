# pylint: disable=C0103
"""Migration file"""

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "1042_registry_username_max_length"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="cap_drop",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=32, null=True),
                blank=True,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="container",
            name="extra_hosts",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=512, null=True),
                blank=True,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="container",
            name="pid_mode",
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name="container",
            name="secOpt",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=512, null=True),
                blank=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="size",
            field=models.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(limit_value=0),
                    django.core.validators.MaxValueValidator(limit_value=8192),
                ],
            ),
        ),
    ]
