# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from netbox_docker_plugin.migrations import netbox_common_fields


fields = [
    (
        "name",
        models.CharField(
            max_length=255,
            validators=[
                django.core.validators.MinLengthValidator(limit_value=1),
                django.core.validators.MaxLengthValidator(limit_value=255),
            ],
        ),
    ),
    (
        "version",
        models.CharField(
            default="latest",
            max_length=32,
            validators=[
                django.core.validators.MinLengthValidator(limit_value=1),
                django.core.validators.MaxLengthValidator(limit_value=32),
            ],
        ),
    ),
    ("provider", models.CharField(default="dockerhub", max_length=32)),
    (
        "host",
        models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name="images",
            to="netbox_docker_plugin.host",
        ),
    ),
]

fields.extend(netbox_common_fields())


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("extras", "0098_webhook_custom_field_data_webhook_tags"),
        ("netbox_docker_plugin", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=fields,
            options={
                "ordering": ("name", "version"),
                "unique_together": {("host", "name", "version")},
            },
        ),
    ]
