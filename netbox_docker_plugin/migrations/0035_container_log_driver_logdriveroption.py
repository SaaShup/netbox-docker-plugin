# pylint: disable=C0103
"""Migration file"""

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "0034_volume_max_size"),
    ]

    operations = [
    ]
