"""Container Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker_plugin.tests.base import BaseModelViewTestCase
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.image import Image


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

        container1 = Container.objects.create(
            host=host1, image=image1, name="container1"
        )
        container2 = Container.objects.create(
            host=host1, image=image1, name="container2"
        )
        Container.objects.create(host=host2, image=image2, name="container3")
        Container.objects.create(host=host2, image=image2, name="container4")

        cls.form_data = {
            "name": "container5",
            "host": host1.pk,
            "image": image1.pk,
            "state": "created",
        }

        cls.csv_data = (
            "name,host,image,hostname",
            f"container6,{host1.pk},{image1.pk},",
            f"container7,{host2.pk},{image2.pk},container7",
        )

        cls.bulk_edit_data = {"state": "running"}

        cls.csv_update_data = (
            "id,name,host,image,state,hostname",
            f"{container1.pk},container1,{host1.pk},{image1.pk},paused,",
            f"{container2.pk},container2,{host1.pk},{image1.pk},running,container2",
        )
