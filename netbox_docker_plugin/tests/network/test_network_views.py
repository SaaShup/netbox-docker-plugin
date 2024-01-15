"""Network Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker_plugin.tests.base import BaseModelViewTestCase
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.network import Network


class NetworkViewsTestCase(
    BaseModelViewTestCase, ViewTestCases.PrimaryObjectViewTestCase
):
    """Network Views Test Case Class"""

    model = Network

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")
        host3 = Host.objects.create(endpoint="http://localhost:8081", name="host3")

        network1 = Network.objects.create(name="network1", host=host1)
        network2 = Network.objects.create(name="network2", host=host2, driver="bridge")
        network3 = Network.objects.create(name="network3", host=host3, driver="host")
        network4 = Network.objects.create(name="network4", host=host3, driver=None)

        cls.form_data = {
            "name": "image5",
            "driver": "bridge",
            "host": host1.pk,
            "NetworkID": "abcdefghijklmnopqrstuvwxyz",
        }

        cls.csv_data = (
            "name,driver,host",
            f"image6,,{host1.pk}",
            f"image7,host,{host2.pk}",
            f"image8,bridge,{host3.pk}",
        )

        cls.bulk_edit_data = {"driver": "host"}

        cls.csv_update_data = (
            "id,driver",
            f"{network1.pk},host",
            f"{network2.pk},",
            f"{network3.pk},bridge",
            f"{network4.pk},host",
        )
