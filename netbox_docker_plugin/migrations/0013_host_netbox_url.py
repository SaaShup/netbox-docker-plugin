# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        ("netbox_docker_plugin", "0012_host_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="host",
            name="netbox_base_url",
            field=models.CharField(
                blank=True,
                max_length=1024,
                null=True,
                validators=[django.core.validators.URLValidator()],
            ),
        ),
    ]
