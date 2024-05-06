""" Container action restrictions test suite """

from django.db import transaction
from django.test import TestCase
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry
from utilities.exceptions import AbortRequest


class ContainerActionTestCase(TestCase):
    """ Test the various scenarii of container actions """

    objects = {}

    def test_delete_non_running_container(self):
        """ Test that a non-running container can be deleted """

        for state in ["created", "paused", "exited", "dead"]:
            with transaction.atomic():
                obj = Container.objects.create(
                    host=self.objects["host"],
                    image=self.objects["image"],
                    name=f"container-{state}",
                    state=state,
                )

                obj.delete()

            self.assertFalse(
                Container.objects.filter(name=f"container-{state}").exists()
            )

    def test_delete_running_container(self):
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

    def test_start_non_running_container(self):
        """ Test that a non-running container can be started """

        for state in ["created", "paused", "exited", "dead"]:
            with transaction.atomic():
                obj = Container.objects.create(
                    host=self.objects["host"],
                    image=self.objects["image"],
                    name=f"container-{state}",
                    state=state,
                )

                obj.operation = "start"
                obj.save()

            self.assertEqual(
                Container.objects.get(name=f"container-{state}").operation,
                "start",
            )

    def test_start_running_container(self):
        """ Test that a running container cannot be started """

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

                    obj.operation = "start"
                    obj.save()

    def test_restart_non_running_container(self):
        """ Test that a non-running container cannot be restarted """

        for state in ["created", "paused", "exited", "dead", "none"]:
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

                    obj.operation = "restart"
                    obj.save()

    def test_restart_running_container(self):
        """ Test that a running container can be restarted """

        for state in ["running", "restarting"]:
            with transaction.atomic():
                obj = Container.objects.create(
                    host=self.objects["host"],
                    image=self.objects["image"],
                    name=f"container-{state}",
                    state=state,
                )

                obj.operation = "restart"
                obj.save()

            self.assertEqual(
                Container.objects.get(name=f"container-{state}").operation,
                "restart",
            )

    def test_stop_non_running_container(self):
        """ Test that a non-running container cannot be stopped """

        for state in ["created", "paused", "exited", "dead", "none"]:
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

                    obj.operation = "stop"
                    obj.save()

    def test_stop_running_container(self):
        """ Test that a running container can be stopped """

        for state in ["running", "restarting"]:
            with transaction.atomic():
                obj = Container.objects.create(
                    host=self.objects["host"],
                    image=self.objects["image"],
                    name=f"container-{state}",
                    state=state,
                )

                obj.operation = "stop"
                obj.save()

            self.assertEqual(
                Container.objects.get(name=f"container-{state}").operation,
                "stop",
            )

    def test_recreate_container(self):
        """ Test that a container can always be recreated """

        for state in ["created", "paused", "exited", "dead", "running", "restarting"]:
            with transaction.atomic():
                obj = Container.objects.create(
                    host=self.objects["host"],
                    image=self.objects["image"],
                    name=f"container-{state}",
                    state=state,
                )

                obj.operation = "recreate"
                obj.save()

            self.assertEqual(
                Container.objects.get(name=f"container-{state}").operation,
                "recreate",
            )

    def test_recreate_none_container(self):
        """ Test that a container in state 'none' cannot be recreated """

        with transaction.atomic():
            with self.assertRaises(
                AbortRequest,
                msg="AbortRequest not raised for 'none'",
            ):
                obj = Container.objects.create(
                    host=self.objects["host"],
                    image=self.objects["image"],
                    name="container-none",
                    state="none",
                )

                obj.operation = "recreate"
                obj.save()

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
