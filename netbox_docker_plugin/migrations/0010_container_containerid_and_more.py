# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "0009_remove_container_network_networksettings_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="ContainerID",
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
                fields=("host", "ContainerID"),
                name="netbox_docker_plugin_container_unique_ContainerID_host",
            ),
        ),
    ]
