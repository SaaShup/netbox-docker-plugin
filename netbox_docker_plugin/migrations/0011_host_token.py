# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("users", "0004_netboxgroup_netboxuser"),
        ("netbox_docker_plugin", "0010_container_containerid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="host",
            name="token",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.token",
            ),
        ),
    ]
