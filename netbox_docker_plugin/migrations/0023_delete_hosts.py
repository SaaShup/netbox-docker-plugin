# pylint: disable=C0103
"""Migration file"""

from django.db import migrations


def delete_hosts(apps, schema_editor):
    """Delete all Hosts and Registries"""
    Host = apps.get_model("netbox_docker_plugin", "Host")
    Host.objects.using(schema_editor.connection.alias).all().delete()

    Registry = Host = apps.get_model("netbox_docker_plugin", "Registry")
    Registry.objects.using(schema_editor.connection.alias).all().delete()


def do_nothing(apps, schema_editor): # pylint: disable=W0613
    """Nothing to do"""
    return None


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        (
            "netbox_docker_plugin",
            "0022_bind_bind_netbox_docker_plugin_bind_unique_bind",
        ),
    ]

    operations = [
        migrations.RunPython(delete_hosts, do_nothing),
    ]
