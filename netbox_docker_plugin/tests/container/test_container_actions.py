""" Container action restrictions test suite """

from django.db import transaction
from django.test import TestCase
from utilities.exceptions import AbortRequest
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry


class ContainerActionTestCase(TestCase):
    """ Test the various scenarii of container actions """

    objects = {}

    def test_allowed_operations(self):
        """ Test that only specific operations are allowed according to a state """

        cases = [
            ("create", ["none"]),
            ("start", ["created", "exited", "dead"]),
            ("stop", ["running"]),
            ("restart", ["running"]),
            ("recreate", ["created", "exited", "dead", "running"]),
            ("noop", ["created", "restarting", "running", "paused", "exited", "dead", "none"]),
        ]

        for operation, states in cases:
            for state in states:
                with self.subTest(operation=operation, state=state):
                    with transaction.atomic():
                        name = f"container-{operation}-{state}"
                        obj = Container.objects.create(
                            host=self.objects["host"],
                            image=self.objects["image"],
                            name=name,
                            operation="none",
                            state=state,
                        )

                        obj.operation = operation
                        obj.save()

                    self.assertEqual(
                        Container.objects.get(name=name).operation,
                        operation,
                    )

    def test_forbidden_operations(self):
        """ Test that forbidden operations raise an AbortRequest """

        cases = [
            ("create", ["created", "restarting", "running", "paused", "exited", "dead"]),
            ("start", ["running", "restarting", "paused", "none"]),
            ("stop", ["created", "restarting", "paused", "exited", "dead", "none"]),
            ("restart", ["created", "restarting", "paused", "exited", "dead", "none"]),
            ("recreate", ["restarting", "paused", "none"]),
        ]

        for operation, states in cases:
            for state in states:
                with self.subTest(operation=operation, state=state):
                    with transaction.atomic():
                        with self.assertRaises(
                            AbortRequest,
                            msg=f"AbortRequest not raised for {state}",
                        ):
                            name = f"container-{operation}-{state}"
                            obj = Container.objects.create(
                                host=self.objects["host"],
                                image=self.objects["image"],
                                name=name,
                                operation="none",
                                state=state,
                            )

                            obj.operation = operation
                            obj.save()

    def test_delete_non_running_container(self):
        """ Test that a non running container can be deleted """

        for state in ["created", "paused", "exited", "dead"]:
            with self.subTest(operation="delete", state=state):
                with transaction.atomic():
                    name = f"container-delete-{state}"
                    obj = Container.objects.create(
                        host=self.objects["host"],
                        image=self.objects["image"],
                        name=name,
                        operation="none",
                        state=state,
                    )

                    obj.delete()

                self.assertFalse(Container.objects.filter(name=name).exists())

    def test_delete_running_container(self):
        """ Test that a running container cannot be deleted """

        for state in ["running", "restarting", "none"]:
            with self.subTest(operation="delete", state=state):
                with transaction.atomic():
                    with self.assertRaises(
                        AbortRequest,
                        msg=f"AbortRequest not raised for {state}",
                    ):
                        name = f"container-delete-{state}"
                        obj = Container.objects.create(
                            host=self.objects["host"],
                            image=self.objects["image"],
                            name=name,
                            operation="none",
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
