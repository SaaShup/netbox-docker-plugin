"""Host Test Case"""

from utilities.testing import APIViewTestCases
from netbox_docker.models import Host
from netbox_docker.tests.base import BaseAPITestCase


class HostTestCase(BaseAPITestCase, APIViewTestCases.GetObjectViewTestCase):
    """Host Test Case Class"""

    model = Host

    @classmethod
    def setUpTestData(cls) -> None:
        Host.objects.create(endpoint="http://localhost:8080", name="test1")
        Host.objects.create(endpoint="http://localhost:8081", name="test2")
