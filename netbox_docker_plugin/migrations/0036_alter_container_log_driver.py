# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0035_container_log_driver_logdriveroption"),
    ]

    operations = [
        migrations.RunSQL(
            "UPDATE netbox_docker_plugin_container "
            + "SET log_driver='json-file' WHERE log_driver='json-log'"
        ),
        migrations.AlterField(
            model_name="container",
            name="log_driver",
            field=models.CharField(default="json-file", max_length=32),
        ),
    ]
