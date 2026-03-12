from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_docker_plugin", "1041_sysctl"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registry",
            name="username",
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
