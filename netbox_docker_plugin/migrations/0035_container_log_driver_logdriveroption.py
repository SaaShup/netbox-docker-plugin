# pylint: disable=C0103
"""Migration file"""

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0034_volume_max_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="log_driver",
            field=models.CharField(default="json-log", max_length=32),
        ),
        migrations.CreateModel(
            name="LogDriverOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "option_name",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=255),
                        ],
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        blank=True,
                        max_length=4096,
                        validators=[
                            django.core.validators.MaxLengthValidator(limit_value=4096)
                        ],
                    ),
                ),
                (
                    "container",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="log_driver_options",
                        to="netbox_docker_plugin.container",
                    ),
                ),
            ],
            options={
                "ordering": ("container", "option_name"),
                "constraints": [
                    models.UniqueConstraint(
                        models.F("option_name"),
                        models.F("container"),
                        name="netbox_docker_plugin_logdriveroption_unique_option_name_container'",
                    )
                ],
            },
        ),
    ]
