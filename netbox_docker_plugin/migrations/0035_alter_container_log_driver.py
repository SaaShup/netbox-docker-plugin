# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ('netbox_docker_plugin', '0034_container_log_driver_logdriveroption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='log_driver',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
