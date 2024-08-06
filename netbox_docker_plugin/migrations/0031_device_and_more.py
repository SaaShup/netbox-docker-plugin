# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0030_container_cap_add"),
    ]

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "host_path",
                    models.CharField(
                        max_length=1024,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=1024),
                        ],
                    ),
                ),
                (
                    "container_path",
                    models.CharField(
                        max_length=1024,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=1024),
                        ],
                    ),
                ),
                (
                    "container",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="devices",
                        to="netbox_docker_plugin.container",
                    ),
                ),
            ],
            options={
                "ordering": ("container", "container_path", "host_path"),
            },
        ),
        migrations.AddConstraint(
            model_name="device",
            constraint=models.UniqueConstraint(
                fields=("container", "container_path", "host_path"),
                name="netbox_docker_plugin_device_unique_device",
            ),
        ),
    ]