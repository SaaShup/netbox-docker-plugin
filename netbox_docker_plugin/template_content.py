"""Template modifications definitions"""

# pylint: disable=W0223

from netbox.plugins import PluginTemplateExtension
from .models import Host


class VirtualMachineHostTable(PluginTemplateExtension):
    """Virtual machine object template"""

    models = ["virtualization.virtualmachine"]

    def right_page(self):
        return self.render(
            "netbox_docker_plugin/virtual_machine_host_table.html",
            extra_context={
                "Host": Host.objects.filter(virtual_machine=self.context["object"])
            },
        )


template_extensions = [VirtualMachineHostTable]
