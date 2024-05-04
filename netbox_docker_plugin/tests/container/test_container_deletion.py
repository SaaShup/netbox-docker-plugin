""" Container deletion test suite """

from django.db import transaction
from django.test import TestCase
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry
from utilities.exceptions import AbortRequest


class ContainerDeletionTestCase(TestCase):
    """ Test the various scenario of container deletion """

    objects = {}

    def test_non_running_container_deletion(self):
        """ Test that a non-running container can be deleted """

        for state in ["created", "paused", "exited", "dead"]:
            obj = Container.objects.create(
                host=self.objects["host"],
                image=self.objects["image"],
                name=f"container-{state}",
                state=state,
            )

            obj.delete()

    def test_running_container_deletetion(self):
        """ Test that a running container cannot be deleted """

        for state in ["running", "restarting", "none"]:
            with transaction.atomic():
                with self.assertRaises(
                    AbortRequest,
                    msg=f"AbortRequest not raised for {state}",
                ):
                    obj = Container.objects.create(
                        host=self.objects["host"],
                        image=self.objects["image"],
                        name=f"container-{state}",
                        state=state,
                    )

                    obj.delete()

    @classmethod
    def setUpTestData(cls):
        cls.objects["host"] = Host.objects.create(
            endpoint="http://localhost:8080",
            name="host",
        )
        cls.objects["registry"] = Registry.objects.create(
            host=cls.objects["host"],
            name="registry",
            serveraddress="http://localhost:8080",
        )
        cls.objects["image"] = Image.objects.create(
            host=cls.objects["host"],
            registry=cls.objects["registry"],
            name="image",
        )
