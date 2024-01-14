# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models
from netbox_docker_plugin.migrations import netbox_common_fields


fields = [
    (
        "endpoint",
        models.CharField(
            max_length=1024,
            validators=[django.core.validators.URLValidator()],
        ),
    ),
    (
        "name",
        models.CharField(
            max_length=255,
            unique=True,
            validators=[
                django.core.validators.MinLengthValidator(limit_value=1),
                django.core.validators.MaxLengthValidator(limit_value=255),
            ],
        ),
    ),
]

fields.extend(netbox_common_fields())


class Migration(migrations.Migration):
    """Migration Class"""

    initial = True

    dependencies = [
        ("extras", "0098_webhook_custom_field_data_webhook_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Host",
            fields=fields,
            options={
                "ordering": ("name",),
            },
        ),
    ]
