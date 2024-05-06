"""Container Validation Test Case"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.volume import Volume
from netbox_docker_plugin.models.network import Network
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.models.container import Mount, NetworkSetting


class ContainerValidationTestCase(TestCase):
    """Container Validation Case Class"""

    objects = {}

    def test_that_container_is_created(self):
        """Test that Container object is created"""

        container = Container.objects.create(
            host=self.objects["host1"],
            image=self.objects["image1"],
            name="container1",
            operation="none",
            state="created",
        )

        self.assertTrue(isinstance(container.id, int))

        container = Container.objects.create(
            host=self.objects["host2"],
            image=self.objects["image2"],
            name="container2",
            operation="none",
            state="created",
        )

        self.assertTrue(isinstance(container.id, int))

    def test_that_container_image_must_be_on_the_same_host(self):
        """Test that Container image must be on the same host"""

        with self.assertRaises(ValidationError) as cm:
            container = Container(
                host=self.objects["host1"],
                image=self.objects["image2"],
                name="container2",
                operation="none",
                state="created",
            )
            container.clean()

        self.assertEqual(
            cm.exception.messages,
            ["Image image2:latest does not belong to host host1."],
        )
        self.assertEqual(
            cm.exception.message_dict["image"],
            ["Image image2:latest does not belong to host host1."],
        )

    def test_that_volume_mounted_must_be_on_the_same_container_host(self):
        """Test that volume mounted must be on the same container host"""

        with self.assertRaises(ValidationError) as cm:
            container = Container(
                host=self.objects["host1"],
                image=self.objects["image1"],
                name="container3",
                operation="none",
                state="created",
            )

            mount = Mount(
                container=container, volume=self.objects["volume2"], source="/data"
            )

            mount.clean()

        self.assertEqual(
            cm.exception.messages,
            ["Volume volume2 does not belong to host host1."],
        )
        self.assertEqual(
            cm.exception.message_dict["volume"],
            ["Volume volume2 does not belong to host host1."],
        )

    def test_that_network_setting_must_be_on_the_same_container_host(self):
        """Test that network settings must be on the same container host"""

        with self.assertRaises(ValidationError) as cm:
            container = Container(
                host=self.objects["host1"],
                image=self.objects["image1"],
                name="container3",
                operation="none",
                state="created",
            )

            network_setting = NetworkSetting(
                container=container, network=self.objects["network2"]
            )

            network_setting.clean()

        self.assertEqual(
            cm.exception.messages,
            ["Network network2 does not belong to host host1."],
        )
        self.assertEqual(
            cm.exception.message_dict["network"],
            ["Network network2 does not belong to host host1."],
        )

    @classmethod
    def setUpTestData(cls) -> None:
        cls.objects["host1"] = Host.objects.create(
            endpoint="http://localhost:8080", name="host1"
        )
        cls.objects["host2"] = Host.objects.create(
            endpoint="http://localhost:8081", name="host2"
        )

        cls.objects["registry1"] = Registry.objects.create(
            host=cls.objects["host1"],
            name="registry1",
            serveraddress="http://localhost:8080",
        )
        cls.objects["registry2"] = Registry.objects.create(
            host=cls.objects["host2"],
            name="registry2",
            serveraddress="http://localhost:8082",
        )

        cls.objects["image1"] = Image.objects.create(
            host=cls.objects["host1"], name="image1", registry=cls.objects["registry1"]
        )
        cls.objects["image2"] = Image.objects.create(
            host=cls.objects["host2"], name="image2", registry=cls.objects["registry2"]
        )

        cls.objects["volume1"] = Volume.objects.create(
            host=cls.objects["host1"], name="volume1"
        )
        cls.objects["volume2"] = Volume.objects.create(
            host=cls.objects["host2"], name="volume2"
        )

        cls.objects["network2"] = Network.objects.create(
            host=cls.objects["host2"], name="network2"
        )
