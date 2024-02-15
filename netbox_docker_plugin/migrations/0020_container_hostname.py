# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0019_host_agent_version_host_docker_api_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="hostname",
            field=models.CharField(
                blank=True,
                max_length=256,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=256),
                ],
            ),
        ),
    ]
