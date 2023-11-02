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

engine_item = [
    PluginMenuItem(
        link="plugins:netbox_docker:host_list",
        link_text="Hosts",
        buttons=host_buttons,
        permissions=["netbox_docker.view_host"]
    ),
    PluginMenuItem(
        link="plugins:netbox_docker:image_list",
        link_text="Images",
        buttons=image_buttons,
        permissions=["netbox_docker.view_image"]
    )
]

menu = PluginMenu(
    label="Docker",
    groups=(("HOST", engine_item),),
    icon_class="mdi mdi-docker",
)
