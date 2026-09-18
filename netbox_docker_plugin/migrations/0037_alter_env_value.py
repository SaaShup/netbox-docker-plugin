# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Raise Env.value to 32768 characters.

    The agent imports environment variables verbatim from the Docker daemon;
    inline configuration and certificate material routinely exceed the previous
    4096 character ceiling.
    """

    dependencies = [
        ("netbox_docker_plugin", "0036_alter_container_log_driver"),
    ]

    operations = [
        migrations.AlterField(
            model_name="env",
            name="value",
            field=models.CharField(
                blank=True,
                max_length=32768,
                validators=[
                    django.core.validators.MaxLengthValidator(limit_value=32768)
                ],
            ),
        ),
    ]
