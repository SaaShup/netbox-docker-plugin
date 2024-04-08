# pylint: disable=C0103
"""Migration file"""

import taggit.managers
import utilities.json
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0020_container_hostname"),
    ]

    operations = [
        migrations.CreateModel(
            name="Registry",
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
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=255),
                        ],
                    ),
                ),
                ("serveraddress", models.URLField()),
                ("username", models.CharField(blank=True, max_length=512, null=True)),
                ("password", models.CharField(blank=True, max_length=512, null=True)),
                ("email", models.EmailField(blank=True, max_length=512, null=True)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.AddField(
            model_name="image",
            name="registry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="netbox_docker_plugin.registry",
            ),
        ),
        migrations.RemoveConstraint(
            model_name="image",
            name="netbox_docker_plugin_image_unique_version_name_host",
        ),
        migrations.RemoveField(
            model_name="image",
            name="provider",
        ),
        migrations.AddConstraint(
            model_name="image",
            constraint=models.UniqueConstraint(
                fields=("host", "registry", "name", "version"),
                name="netbox_docker_plugin_image_unique_version_name_registry_host",
            ),
        ),
        migrations.AddField(
            model_name="registry",
            name="tags",
            field=taggit.managers.TaggableManager(
                through="extras.TaggedItem", to="extras.Tag"
            ),
        ),
    ]
