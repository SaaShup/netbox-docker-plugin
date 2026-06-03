# pylint: disable=C0103
"""Migration file"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "1043_container_cap_drop_container_extra_hosts_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="host",
            name="virtual_machine",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="virtualization.virtualmachine",
            ),
        ),
    ]
