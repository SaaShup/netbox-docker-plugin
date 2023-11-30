"""Volume Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker.tests.base import BaseModelViewTestCase
from netbox_docker.models.host import Host
from netbox_docker.models.container import Container
from netbox_docker.models.network import Network
from netbox_docker.models.image import Image


class ContainerViewsTestCase(
    BaseModelViewTestCase, ViewTestCases.PrimaryObjectViewTestCase
):
    """Container Views Test Case Class"""

    model = Container

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")

        image1 = Image.objects.create(host=host1, name="image1")
        image2 = Image.objects.create(host=host2, name="image2")

        network1 = Network.objects.create(host=host1, name="network1")
        network2 = Network.objects.create(host=host2, name="network2")

        container1 = Container.objects.create(
            host=host1, image=image1, network=network1, name="container1"
        )
        container2 = Container.objects.create(
            host=host1, image=image1, network=network1, name="container2"
        )
        Container.objects.create(
            host=host2, image=image2, network=network2, name="container3"
        )
        Container.objects.create(host=host2, image=image2, name="container4")

        cls.form_data = {
            "name": "container5",
            "host": host1.pk,
            "image": image1.pk,
            "network": network1.pk,
        }

        cls.csv_data = (
            "name,host,image,network",
            f"container6,{host1.pk},{image1.pk},{network1.pk}",
            f"container7,{host2.pk},{image2.pk},",
        )

        cls.bulk_edit_data = {"state": "running"}

        cls.csv_update_data = (
            "id,name,host,image,network,state",
            f"{container1.pk},container1,{host1.pk},{image1.pk},{network1.pk},paused",
            f"{container2.pk},container2,{host1.pk},{image1.pk},{network1.pk},running",
        )
