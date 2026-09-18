# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Allow Port.public_port to be -1.

    The agent uses -1 to mean "exposed but not published"; the previous floor
    of 0 rejected every container with an unpublished exposed port.
    """

    dependencies = [
        ("netbox_docker_plugin", "0037_alter_env_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="port",
            name="public_port",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(limit_value=-1),
                    django.core.validators.MaxValueValidator(limit_value=65535),
                ]
            ),
        ),
    ]
