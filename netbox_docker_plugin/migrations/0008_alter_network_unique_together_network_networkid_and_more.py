# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "0007_remove_container_netbox_docker_plugin_container_unique_name_host__and_more",
        ),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="network",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="network",
            name="NetworkID",
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
            model_name="network",
            constraint=models.UniqueConstraint(
                fields=("host", "name"),
                name="netbox_docker_plugin_network_unique_name_host",
            ),
        ),
        migrations.AddConstraint(
            model_name="network",
            constraint=models.UniqueConstraint(
                fields=("host", "NetworkID"),
                name="netbox_docker_plugin_network_unique_NetworkID_host",
            ),
        ),
    ]
