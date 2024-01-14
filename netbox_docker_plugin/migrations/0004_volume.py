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
                django.core.validators.MinLengthValidator(limit_value=3),
                django.core.validators.MaxLengthValidator(limit_value=255),
            ],
        ),
    ),
    ("driver", models.CharField(default="local", max_length=32)),
    (
        "host",
        models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name="volumes",
            to="netbox_docker_plugin.host",
        ),
    ),
]

fields.extend(netbox_common_fields())


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("extras", "0098_webhook_custom_field_data_webhook_tags"),
        ("netbox_docker_plugin", "0003_image_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="Volume",
            fields=fields,
            options={
                "ordering": ("name",),
                "unique_together": {("host", "name")},
            },
        ),
    ]
