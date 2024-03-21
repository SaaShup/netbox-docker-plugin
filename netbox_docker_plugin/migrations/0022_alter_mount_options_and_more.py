# pylint: disable=C0103
""" Migration file """

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0021_registry_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mount",
            options={"ordering": ("container", "source")},
        ),
        migrations.RemoveConstraint(
            model_name="mount",
            name="netbox_docker_plugin_mount_unique_volume",
        ),
        migrations.AddField(
            model_name="mount",
            name="host_path",
            field=models.CharField(
                max_length=1024,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=1024),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="mount",
            name="volume",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="mounts",
                to="netbox_docker_plugin.volume",
            ),
        ),
        migrations.AddConstraint(
            model_name="mount",
            constraint=models.UniqueConstraint(
                fields=("container", "source"), name="netbox_docker_plugin_mount_unique"
            ),
        ),
        migrations.AlterField(
            model_name="mount",
            name="host_path",
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddConstraint(
            model_name="mount",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("host_path__isnull", False), ("volume__isnull", False)),
                    models.Q(("host_path__isnull", True), ("volume__isnull", True)),
                    models.Q(("host_path__length", 0), ("volume__isnull", True)),
                    _connector="OR",
                    _negated=True,
                ),
                name="netbox_docker_plugin_mount_volume_or_hostpath",
                violation_error_message="Either volume or host path must be set.",
            ),
        ),
        migrations.AlterField(
            model_name="mount",
            name="host_path",
            field=models.CharField(
                default=None,
                max_length=1024,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=1024),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="mount",
            name="volume",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="mounts",
                to="netbox_docker_plugin.volume",
            ),
        ),
        migrations.RemoveConstraint(
            model_name="mount",
            name="netbox_docker_plugin_mount_volume_or_hostpath",
        ),
        migrations.AddConstraint(
            model_name="mount",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("host_path__isnull", False),
                    ("host_path__length__gt", 0),
                    ("volume__isnull", False),
                    _negated=True,
                ),
                name="netbox_docker_plugin_mount_volume_or_host_path_set",
                violation_error_message=(
                    "The volume and host path cannot be both set at the same time."
                ),
            ),
        ),
        migrations.AddConstraint(
            model_name="mount",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("host_path__isnull", True), ("volume__isnull", True)),
                    models.Q(("host_path__length", 0), ("volume__isnull", True)),
                    _connector="OR",
                    _negated=True,
                ),
                name="netbox_docker_plugin_mount_volume_or_host_path_unset",
                violation_error_message="At least one of the volume or host path must be set.",
            ),
        ),
        migrations.RemoveConstraint(
            model_name="mount",
            name="netbox_docker_plugin_mount_volume_or_host_path_set",
        ),
        migrations.RemoveConstraint(
            model_name="mount",
            name="netbox_docker_plugin_mount_volume_or_host_path_unset",
        ),
        migrations.AlterField(
            model_name="mount",
            name="host_path",
            field=models.CharField(default=None, max_length=1024, null=True),
        ),
        migrations.AddConstraint(
            model_name="mount",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("host_path__isnull", False),
                    ("host_path__length__gt", 0),
                    ("volume__isnull", False),
                    _negated=True,
                ),
                name="netbox_docker_plugin_mount_volume_or_host_path_set",
                violation_error_message="Only one of the volume or host path must be set.",
            ),
        ),
        migrations.AddConstraint(
            model_name="mount",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("host_path__isnull", True), ("volume__isnull", True)),
                    models.Q(("host_path__length", 0), ("volume__isnull", True)),
                    _connector="OR",
                    _negated=True,
                ),
                name="netbox_docker_plugin_mount_volume_or_host_path_unset",
                violation_error_message="At least one of the volume or host path must be set.",
            ),
        ),
    ]
