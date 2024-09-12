# pylint: disable=R0801
"""Container Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker_plugin.tests.base import BaseModelViewTestCase
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry


class ContainerViewsTestCase(
    BaseModelViewTestCase, ViewTestCases.PrimaryObjectViewTestCase
):
    """Container Views Test Case Class"""

    model = Container

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")

        registry1 = Registry.objects.create(
            host=host1, name="registry1", serveraddress="http://localhost:8080"
        )
        registry2 = Registry.objects.create(
            host=host2, name="registry2", serveraddress="http://localhost:8082"
        )

        image1 = Image.objects.create(host=host1, name="image1", registry=registry1)
        image2 = Image.objects.create(host=host2, name="image2", registry=registry2)

        container1 = Container.objects.create(
            host=host1,
            image=image1,
            name="container1",
            restart_policy="always",
            operation="none",
            state="created",
        )
        container2 = Container.objects.create(
            host=host1,
            image=image1,
            name="container2",
            operation="none",
            state="created",
        )
        Container.objects.create(
            host=host2,
            image=image2,
            name="container3",
            operation="none",
            state="created",
        )
        Container.objects.create(
            host=host2,
            image=image2,
            name="container4",
            operation="none",
            state="created",
        )

        cls.form_data = {
            "name": "container5",
            "host": host1.pk,
            "image": image1.pk,
            "restart_policy": "unless-stopped",
            "cap_add": ["NET_ADMIN"],
        }

        cls.csv_data = (
            "name,host,image,hostname",
            f"container6,{host1.pk},{image1.pk},",
            f"container7,{host2.pk},{image2.pk},container7",
        )

        cls.bulk_edit_data = {
            "hostname": "h",
            "restart_policy": "always",
        }

        cls.csv_update_data = (
            "id,name,host,image,hostname,restart_policy",
            f"{container1.pk},container1,{host1.pk},{image1.pk},,on-failure",
            f"{container2.pk},container2,{host1.pk},{image1.pk},container2,unless-stopped",
        )
