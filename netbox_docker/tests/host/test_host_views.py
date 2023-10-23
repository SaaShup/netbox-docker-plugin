"""Host Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker.tests.base import BaseModelViewTestCase
from netbox_docker.models import Host


class HostViewsTestCase(
    BaseModelViewTestCase,
    ViewTestCases.PrimaryObjectViewTestCase
):
    """Host Views Test Case Class"""

    model = Host
    form_data = {
        "name": "host4",
        "endpoint": "http://localhost:8084",
    }
    csv_data = (
        "name,endpoint",
        "host5,http://localhost:8084",
        "host6,http://localhost:8084",
        "host7,http://localhost:8084",
    )
    bulk_edit_data = {"endpoint": "http://localhost:8083"}

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")
        host3 = Host.objects.create(endpoint="http://localhost:8081", name="host3")

        cls.csv_update_data = (
            "id,endpoint",
            f"{host1.pk},http://localhost:8085",
            f"{host2.pk},http://localhost:8085",
            f"{host3.pk},http://localhost:8085",
        )
