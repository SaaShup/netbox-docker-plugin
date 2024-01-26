"""Network Test Case"""

from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.network import Network
from netbox_docker_plugin.tests.base import BaseAPITestCase


class NetworkApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Network Test Case Class"""

    model = Network
    brief_fields = ["NetworkID", "display", "driver", "id", "name", "state", "url"]

    @classmethod
    def setUpTestData(cls) -> None:
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        Network.objects.create(host=host1, name="network1")
        Network.objects.create(host=host1, name="network2", driver="bridge")
        Network.objects.create(host=host2, name="network3", driver="host")
        Network.objects.create(host=host2, name="network4", driver=None)

        cls.create_data = [
            {"host": host1.pk, "name": "network5"},
            {
                "host": host1.pk,
                "name": "network6",
                "driver": "bridge",
            },
            {
                "host": host2.pk,
                "name": "network7",
                "driver": "host",
            },
            {
                "host": host2.pk,
                "name": "network8",
                "driver": None,
            },
        ]
