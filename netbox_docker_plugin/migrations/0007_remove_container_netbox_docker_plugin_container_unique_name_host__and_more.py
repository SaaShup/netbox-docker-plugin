# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("netbox_docker_plugin", "0006_container_port_mount_label_env_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="container",
            name="netbox_docker_plugin_container_unique_name_host'",
        ),
        migrations.AlterUniqueTogether(
            name="image",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="image",
            name="ImageID",
            field=models.CharField(
                blank=True,
                max_length=128,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=128),
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name="container",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                models.F("host"),
                name="netbox_docker_plugin_container_unique_name_host",
            ),
        ),
        migrations.AddConstraint(
            model_name="image",
            constraint=models.UniqueConstraint(
                fields=("host", "name", "version"),
                name="netbox_docker_plugin_image_unique_version_name_host",
            ),
        ),
        migrations.AddConstraint(
            model_name="image",
            constraint=models.UniqueConstraint(
                fields=("host", "ImageID"),
                name="netbox_docker_plugin_image_unique_ImageID_host",
            ),
        ),
    ]
