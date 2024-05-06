# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0028_mount_and_bind_read_only"),
    ]

    operations = [
        migrations.AlterField(
            model_name="container",
            name="state",
            field=models.CharField(default="none", max_length=32),
        ),
    ]
