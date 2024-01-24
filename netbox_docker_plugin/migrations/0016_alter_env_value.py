# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "0015_remove_mount_netbox_docker_plugin_mount_unique_volume_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="env",
            name="value",
            field=models.CharField(
                blank=True,
                max_length=4096,
                validators=[
                    django.core.validators.MaxLengthValidator(limit_value=4096)
                ],
            ),
        ),
    ]
