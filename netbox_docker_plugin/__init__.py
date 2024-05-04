"""Netbox Plugin Configuration"""

from extras.plugins import PluginConfig
from django.db.models.signals import post_migrate
from .utilities import create_webhook

class NetBoxDockerConfig(PluginConfig):
    """Plugin Config Class"""

    name = "netbox_docker_plugin"
    verbose_name = " NetBox Docker Plugin"
    description = "Manage Docker"
    version = "1.7.0"
    base_url = "docker"
    author= "Vincent Simonin"
    author_email= "vincent@saashup.com"

    def ready(self):
        from . import signals # pylint: disable=unused-import, import-outside-toplevel

        post_migrate.connect(create_webhook)

        super().ready()


# pylint: disable=C0103
config = NetBoxDockerConfig
