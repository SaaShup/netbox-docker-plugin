"""Navigation Menu definitions"""

from netbox.plugins import (
    PluginMenu,
    PluginMenuItem,
    PluginMenuButton,
)

host_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:host_add",
        title="Add",
        icon_class="mdi mdi-plus-thick"
    ),
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:host_bulk_import",
        title="Import",
        icon_class="mdi mdi-upload"
    ),
]

registry_button = [
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:registry_add",
        title="Add",
        icon_class="mdi mdi-plus-thick"
    ),
]

image_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:image_add",
        title="Add",
        icon_class="mdi mdi-plus-thick"
    ),
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:image_bulk_import",
        title="Import",
        icon_class="mdi mdi-upload"
    ),
]

volume_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:volume_add",
        title="Add",
        icon_class="mdi mdi-plus-thick"
    ),
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:volume_bulk_import",
        title="Import",
        icon_class="mdi mdi-upload"
    ),
]

network_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:network_add",
        title="Add",
        icon_class="mdi mdi-plus-thick"
    ),
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:network_bulk_import",
        title="Import",
        icon_class="mdi mdi-upload"
    ),
]

container_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:container_add",
        title="Add",
        icon_class="mdi mdi-plus-thick"
    ),
    PluginMenuButton(
        link="plugins:netbox_docker_plugin:container_bulk_import",
        title="Import",
        icon_class="mdi mdi-upload"
    ),
]

host_item = [
    PluginMenuItem(
        link="plugins:netbox_docker_plugin:host_list",
        link_text="Hosts",
        buttons=host_buttons,
        permissions=["netbox_docker_plugin.view_host"],
    ),
    PluginMenuItem(
        link="plugins:netbox_docker_plugin:registry_list",
        link_text="Registries",
        buttons=registry_button,
        permissions=["netbox_docker_plugin.view_registry"],
    ),
    PluginMenuItem(
        link="plugins:netbox_docker_plugin:image_list",
        link_text="Images",
        buttons=image_buttons,
        permissions=["netbox_docker_plugin.view_image"],
    ),
    PluginMenuItem(
        link="plugins:netbox_docker_plugin:volume_list",
        link_text="Volumes",
        buttons=volume_buttons,
        permissions=["netbox_docker_plugin.view_volume"],
    ),
    PluginMenuItem(
        link="plugins:netbox_docker_plugin:network_list",
        link_text="Networks",
        buttons=network_buttons,
        permissions=["netbox_docker_plugin.view_network"],
    ),
    PluginMenuItem(
        link="plugins:netbox_docker_plugin:container_list",
        link_text="Containers",
        buttons=container_buttons,
        permissions=["netbox_docker_plugin.view_container"],
    ),
]

menu = PluginMenu(
    label="Docker",
    groups=(("DOCKER", host_item),),
    icon_class="mdi mdi-docker",
)
