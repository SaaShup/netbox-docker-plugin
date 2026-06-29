# pylint: disable=C0103
"""Reverse migration for log_driver and LogDriverOption only"""

from django.db import migrations


class Migration(migrations.Migration):
    """Reverse migration (partial)"""

    dependencies = [
        ("netbox_docker_plugin", "0034_container_log_driver_alter_container_containerid_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
DROP INDEX IF EXISTS public.netbox_docker_plugin_logdriveroption_unique_option_name_contain;
DROP INDEX IF EXISTS public.netbox_docker_plugin_logdriveroption_container_id_929d4dfe;
DROP TABLE IF EXISTS public.netbox_docker_plugin_logdriveroption;
            """,
            state_operations=[
                migrations.DeleteModel(
                    name="LogDriverOption",
                ),
            ],
        ),
        migrations.RunSQL(
            sql="""
ALTER TABLE netbox_docker_plugin_container
DROP COLUMN IF EXISTS log_driver;
            """,
            state_operations=[
                migrations.RemoveField(
                    model_name="container",
                    name="log_driver",
                ),
            ],
        ),
    ]
