"""Navigation Menu definitions"""

from extras.plugins import (
    PluginMenu,
    PluginMenuItem,
    PluginMenuButton,
)
from utilities.choices import ButtonColorChoices

host_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker:host_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link="plugins:netbox_docker:host_import",
        title="Import",
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

image_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker:image_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link="plugins:netbox_docker:image_import",
        title="Import",
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

volume_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker:volume_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link="plugins:netbox_docker:volume_import",
        title="Import",
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

network_buttons = [
    PluginMenuButton(
        link="plugins:netbox_docker:network_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link="plugins:netbox_docker:network_import",
        title="Import",
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

host_item = [
    PluginMenuItem(
        link="plugins:netbox_docker:host_list",
        link_text="Hosts",
        buttons=host_buttons,
        permissions=["netbox_docker.view_host"],
    ),
    PluginMenuItem(
        link="plugins:netbox_docker:image_list",
        link_text="Images",
        buttons=image_buttons,
        permissions=["netbox_docker.view_image"],
    ),
    PluginMenuItem(
        link="plugins:netbox_docker:volume_list",
        link_text="Volumes",
        buttons=volume_buttons,
        permissions=["netbox_docker.view_volume"],
    ),
    PluginMenuItem(
        link="plugins:netbox_docker:network_list",
        link_text="Networks",
        buttons=network_buttons,
        permissions=["netbox_docker.view_network"],
    ),
]

menu = PluginMenu(
    label="Docker",
    groups=(("DOCKER", host_item),),
    icon_class="mdi mdi-docker",
)
