# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Make Container.log_driver a free-form value.

    The agent reports HostConfig.LogConfig.Type verbatim from the Docker
    daemon (json-file, journald, local, ...), which the previous two-value
    choice set rejected. The legacy `json-log` value was never a valid Docker
    driver name and is normalised to `json-file`.
    """

    dependencies = [
        ("netbox_docker_plugin", "0035_container_log_driver_logdriveroption"),
    ]

    operations = [
        migrations.RunSQL(
            sql="UPDATE netbox_docker_plugin_container "
            "SET log_driver='json-file' WHERE log_driver='json-log'",
            reverse_sql="UPDATE netbox_docker_plugin_container "
            "SET log_driver='json-log' WHERE log_driver='json-file'",
        ),
        migrations.AlterField(
            model_name="container",
            name="log_driver",
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
    ]
