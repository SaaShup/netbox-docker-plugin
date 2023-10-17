from extras.plugins import PluginConfig


class NetBoxDockerConfig(PluginConfig):
    """Plugin Config Class"""
    name = 'netbox_docker'
    verbose_name = ' NetBox Docker Plugin'
    description = 'Manage Docker'
    version = '0.0.2'
    base_url = 'docker'


config = NetBoxDockerConfig
