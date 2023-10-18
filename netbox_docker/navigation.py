"""Navigation Menu definitions"""

from extras.plugins import (
    PluginMenu,
    PluginMenuItem,
    PluginMenuButton,
)
from utilities.choices import ButtonColorChoices

engine_buttons = [
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

engine_item = [
    PluginMenuItem(
        link="plugins:netbox_docker:host_list",
        link_text="Hosts",
        buttons=engine_buttons,
        permissions=["netbox_docker.view_host"]
    )
]

menu = PluginMenu(
    label="Docker",
    groups=(("HOST", engine_item),),
    icon_class="mdi mdi-docker",
)
