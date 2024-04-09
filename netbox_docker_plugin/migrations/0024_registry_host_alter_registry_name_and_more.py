# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "0023_delete_hosts",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="registry",
            name="host",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="registries",
                to="netbox_docker_plugin.host",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="registry",
            name="name",
            field=models.CharField(
                max_length=255,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=255),
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name="registry",
            constraint=models.UniqueConstraint(
                fields=("host", "name"), name="netbox_docker_plugin_registry_name_host"
            ),
        ),
    ]
