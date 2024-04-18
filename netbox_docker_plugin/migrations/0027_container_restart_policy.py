# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0026_image_digest"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="restart_policy",
            field=models.CharField(default="no", max_length=32),
        ),
    ]
