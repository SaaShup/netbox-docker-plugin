# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migration Class"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "0008_alter_network_unique_together_network_networkid_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="container",
            name="network",
        ),
        migrations.CreateModel(
            name="NetworkSetting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "container",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="network_settings",
                        to="netbox_docker_plugin.container",
                    ),
                ),
                (
                    "network",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="netbox_docker_plugin.network",
                    ),
                ),
            ],
            options={
                "ordering": ("container", "network"),
            },
        ),
        migrations.AddConstraint(
            model_name="networksetting",
            constraint=models.UniqueConstraint(
                fields=("container", "network"),
                name="netbox_docker_plugin_networksetting_unique_container_network",
            ),
        ),
        migrations.AlterField(
            model_name="label",
            name="value",
            field=models.CharField(
                blank=True,
                max_length=4095,
                validators=[
                    django.core.validators.MaxLengthValidator(limit_value=4095)
                ],
            ),
        ),
    ]
