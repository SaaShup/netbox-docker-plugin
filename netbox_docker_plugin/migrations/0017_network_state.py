# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ('netbox_docker_plugin', '0016_alter_env_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='state',
            field=models.CharField(default='creating', max_length=32),
        ),
    ]
