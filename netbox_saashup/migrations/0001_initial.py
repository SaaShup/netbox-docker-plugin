"""Initial Migration File"""

import django.core.validators
from django.db import migrations, models
import taggit.managers
import utilities.json


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("extras", "0098_webhook_custom_field_data_webhook_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Engine",
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
                    "domain",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=2),
                            django.core.validators.MaxLengthValidator(limit_value=255),
                        ],
                    ),
                ),
                (
                    "port",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=1),
                            django.core.validators.MaxValueValidator(limit_value=65535),
                        ]
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
                "ordering": ("domain",),
                "unique_together": {("domain", "port")},
            },
        ),
    ]
