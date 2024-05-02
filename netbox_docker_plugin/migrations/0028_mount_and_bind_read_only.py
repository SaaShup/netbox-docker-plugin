# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0027_container_restart_policy"),
    ]

    operations = [
        migrations.AddField(
            model_name="mount",
            name="read_only",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="bind",
            name="read_only",
            field=models.BooleanField(default=False),
        ),
    ]
