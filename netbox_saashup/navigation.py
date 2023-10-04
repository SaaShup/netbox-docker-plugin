"""Navigation Menu definitions"""

from extras.plugins import (
    PluginMenu,
    PluginMenuItem,
    PluginMenuButton,
)
from utilities.choices import ButtonColorChoices

engine_buttons = [
    PluginMenuButton(
        link="plugins:netbox_saashup:engine_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
    PluginMenuButton(
        link="plugins:netbox_saashup:engine_add",
        title="Import",
        icon_class="mdi mdi-upload",
        color=ButtonColorChoices.CYAN,
    ),
]

engine_item = [
    PluginMenuItem(
        link="plugins:netbox_saashup:engine_list",
        link_text="Engines",
        buttons=engine_buttons,
    )
]

menu = PluginMenu(
    label="SaaShup",
    groups=(("ENGINES", engine_item),),
    icon_class="mdi mdi-engine",
)
