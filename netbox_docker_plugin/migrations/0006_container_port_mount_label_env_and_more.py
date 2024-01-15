# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
from netbox_docker_plugin.migrations import netbox_common_fields


fields = [
    (
        "name",
        models.CharField(
            max_length=255,
            validators=[
                django.core.validators.MinLengthValidator(limit_value=1),
                django.core.validators.MaxLengthValidator(limit_value=255),
            ],
        ),
    ),
    ("state", models.CharField(default="created", max_length=32)),
    ("status", models.CharField(blank=True, max_length=1024, null=True)),
    (
        "host",
        models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name="containers",
            to="netbox_docker_plugin.host",
        ),
    ),
    (
        "image",
        models.ForeignKey(
            on_delete=django.db.models.deletion.RESTRICT,
            related_name="containers",
            to="netbox_docker_plugin.image",
        ),
    ),
    (
        "network",
        models.ForeignKey(
            null=True,
            blank=True,
            on_delete=django.db.models.deletion.RESTRICT,
            related_name="containers",
            to="netbox_docker_plugin.network",
        ),
    ),
]

fields.extend(netbox_common_fields())


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("extras", "0098_webhook_custom_field_data_webhook_tags"),
        ("netbox_docker_plugin", "0005_network"),
    ]

    operations = [
        migrations.CreateModel(
            name="Container",
            fields=fields,
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Port",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "private_port",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=0),
                            django.core.validators.MaxValueValidator(limit_value=65535),
                        ]
                    ),
                ),
                (
                    "public_port",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=0),
                            django.core.validators.MaxValueValidator(limit_value=65535),
                        ]
                    ),
                ),
                ("type", models.CharField(default="tcp", max_length=3)),
                (
                    "container",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ports",
                        to="netbox_docker_plugin.container",
                    ),
                ),
            ],
            options={
                "ordering": ("container",),
            },
        ),
        migrations.CreateModel(
            name="Mount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=1024,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=1024),
                        ],
                    ),
                ),
                (
                    "container",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mounts",
                        to="netbox_docker_plugin.container",
                    ),
                ),
                (
                    "volume",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="netbox_docker_plugin.volume",
                    ),
                ),
            ],
            options={
                "ordering": ("container", "source", "volume"),
            },
        ),
        migrations.CreateModel(
            name="Label",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "key",
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
                        max_length=4095,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=4095),
                        ],
                    ),
                ),
                (
                    "container",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="labels",
                        to="netbox_docker_plugin.container",
                    ),
                ),
            ],
            options={
                "ordering": ("container", "key"),
            },
        ),
        migrations.CreateModel(
            name="Env",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "var_name",
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
                        max_length=4096,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=4096),
                        ],
                    ),
                ),
                (
                    "container",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="env",
                        to="netbox_docker_plugin.container",
                    ),
                ),
            ],
            options={
                "ordering": ("container", "var_name"),
            },
        ),
        migrations.AddConstraint(
            model_name="port",
            constraint=models.UniqueConstraint(
                models.F("private_port"),
                models.F("public_port"),
                models.F("type"),
                models.F("container"),
                name="netbox_docker_plugin_port_unique_private_port_public_port_type_container'",
            ),
        ),
        migrations.AddConstraint(
            model_name="mount",
            constraint=models.UniqueConstraint(
                fields=("volume",), name="netbox_docker_plugin_mount_unique_volume"
            ),
        ),
        migrations.AddConstraint(
            model_name="label",
            constraint=models.UniqueConstraint(
                models.F("key"),
                models.F("container"),
                name="netbox_docker_plugin_label_unique_key_container'",
            ),
        ),
        migrations.AddConstraint(
            model_name="env",
            constraint=models.UniqueConstraint(
                models.F("var_name"),
                models.F("container"),
                name="netbox_docker_plugin_env_unique_var_name_container'",
            ),
        ),
        migrations.AddConstraint(
            model_name="container",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                models.F("host"),
                name="netbox_docker_plugin_container_unique_name_host'",
            ),
        ),
    ]
