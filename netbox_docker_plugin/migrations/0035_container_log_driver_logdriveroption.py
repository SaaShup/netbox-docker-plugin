# pylint: disable=C0103,C0116,W0613
"""Migration file"""

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models, connection


def apply_database_changes(apps, schema_editor):
    table_container = "netbox_docker_plugin_container"
    table_logdriveroption = "netbox_docker_plugin_logdriveroption"
    index_name = "netbox_docker_plugin_logdriveroption_unique_option_name_contain"

    with connection.cursor() as cursor:
        existing_tables = connection.introspection.table_names(cursor)

        if table_container in existing_tables:
            columns = {
                col.name
                for col in connection.introspection.get_table_description(
                    cursor, table_container
                )
            }
            if "log_driver" not in columns:
                cursor.execute(
                    f"ALTER TABLE {table_container} "
                    "ADD COLUMN log_driver varchar(32) NOT NULL DEFAULT 'json-log'"
                )

        if table_logdriveroption not in existing_tables:
            cursor.execute(
                f"""
                CREATE TABLE {table_logdriveroption} (
                    id bigserial PRIMARY KEY,
                    option_name varchar(255) NOT NULL,
                    value varchar(4096) NOT NULL DEFAULT '',
                    container_id bigint NOT NULL
                        REFERENCES {table_container}(id)
                        ON DELETE CASCADE
                )
                """
            )

        constraints = (
            connection.introspection.get_constraints(cursor, table_logdriveroption)
            if table_logdriveroption in connection.introspection.table_names(cursor)
            else {}
        )
        if index_name not in constraints:
            cursor.execute(
                f"""
                CREATE UNIQUE INDEX {index_name}
                ON {table_logdriveroption} (container_id, option_name)
                """
            )


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0034_volume_max_size"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(apply_database_changes, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="container",
                    name="log_driver",
                    field=models.CharField(default="json-log", max_length=32),
                ),
                migrations.CreateModel(
                    name="LogDriverOption",
                    fields=[
                        (
                            "id",
                            models.BigAutoField(
                                auto_created=True, primary_key=True, serialize=False
                            ),
                        ),
                        (
                            "option_name",
                            models.CharField(
                                max_length=255,
                                validators=[
                                    django.core.validators.MinLengthValidator(limit_value=1),
                                    django.core.validators.MaxLengthValidator(limit_value=255),
                                ],
                            ),
                        ),
                        (
                            "value",
                            models.CharField(
                                blank=True,
                                max_length=4096,
                                validators=[
                                    django.core.validators.MaxLengthValidator(limit_value=4096)
                                ],
                            ),
                        ),
                        (
                            "container",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="log_driver_options",
                                to="netbox_docker_plugin.container",
                            ),
                        ),
                    ],
                    options={
                        "ordering": ("container", "option_name"),
                    },
                ),
                migrations.AddConstraint(
                    model_name="logdriveroption",
                    constraint=models.UniqueConstraint(
                        fields=("option_name", "container"),
                        name="netbox_docker_plugin_logdriveroption_unique_option_name_container",
                    ),
                ),
            ],
        ),
    ]
