# pylint: disable=C0103
""" Migration file """

from django.db import migrations, models


class Migration(migrations.Migration):
    """ Migration file """

    dependencies = [
        ('netbox_docker_plugin', '0022_alter_mount_options_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='mount',
            name='netbox_docker_plugin_mount_volume_or_host_path_set',
        ),
        migrations.RemoveConstraint(
            model_name='mount',
            name='netbox_docker_plugin_mount_volume_or_host_path_unset',
        ),
        migrations.AlterField(
            model_name='mount',
            name='host_path',
            field=models.CharField(blank=True, default='', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='mount',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('host_path__length__gt', 0),
                    ('volume__isnull', False),
                    _negated=True,
                ),
                name='netbox_docker_plugin_mount_volume_or_host_path_set',
                violation_error_message=(
                    'Only one of the volume or host path must be set.'
                ),
            ),
        ),
        migrations.AddConstraint(
            model_name='mount',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('host_path__length', 0),
                    ('volume__isnull', True),
                    _negated=True,
                ),
                name='netbox_docker_plugin_mount_volume_or_host_path_unset',
                violation_error_message=(
                    'At least one of the volume or host path must be set.'
                ),
            ),
        ),
    ]
