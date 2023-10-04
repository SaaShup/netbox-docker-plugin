from extras.plugins import PluginConfig


class NetBoxSaashupConfig(PluginConfig):
    name = 'netbox_saashup'
    verbose_name = ' NetBox SaaShup'
    description = 'Manage SaaShup Engine'
    version = '0.0.1'
    base_url = 'saashup'


config = NetBoxSaashupConfig
