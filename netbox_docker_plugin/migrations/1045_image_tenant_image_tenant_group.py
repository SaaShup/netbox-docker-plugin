# pylint: disable=C0103
"""Migration file"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_docker_plugin", "1044_host_virtual_machine"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="tenancy.tenant",
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="tenant_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="tenancy.tenantgroup",
            ),
        ),
    ]
