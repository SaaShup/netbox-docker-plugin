# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0017_network_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mount",
            name="volume",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="mounts",
                to="netbox_docker_plugin.volume",
            ),
        ),
        migrations.AlterField(
            model_name="networksetting",
            name="network",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="network_settings",
                to="netbox_docker_plugin.network",
            ),
        ),
    ]
