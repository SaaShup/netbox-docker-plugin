# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import utilities.json


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("extras", "0098_webhook_custom_field_data_webhook_tags"),
        ("netbox_docker", "0003_image_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="Volume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
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
                        to="netbox_docker.host",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "unique_together": {("host", "name")},
            },
        ),
    ]
