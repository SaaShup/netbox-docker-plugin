"""Netbox Plugin Configuration"""

from extras.plugins import PluginConfig


class NetBoxDockerConfig(PluginConfig):
    """Plugin Config Class"""

    name = "netbox_docker_plugin"
    verbose_name = " NetBox Docker Plugin"
    description = "Manage Docker"
    version = "1.0.0-rc2"
    base_url = "docker"


# pylint: disable=C0103
config = NetBoxDockerConfig
