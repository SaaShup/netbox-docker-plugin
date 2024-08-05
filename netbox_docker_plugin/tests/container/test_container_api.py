# pylint: disable=R0801
"""Container Test Case"""

import requests_mock
from django.urls import reverse
from core.models import ObjectType
from rest_framework import status
from users.models import ObjectPermission
from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.container import Container, Bind, Env
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.network import Network
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.volume import Volume
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.tests.base import BaseAPITestCase


class ContainerApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Container Test Case Class"""

    model = Container
    brief_fields = [
        "ContainerID",
        "cap_add",
        "display",
        "hostname",
        "id",
        "name",
        "operation",
        "restart_policy",
        "state",
        "status",
        "url",
    ]
    validation_excluded_fields = [
        "ports",
        "env",
        "labels",
        "mounts",
        "binds",
        "network_settings",
        "devices",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        registry1 = Registry.objects.create(
            host=host1, name="registry1", serveraddress="http://localhost:8080"
        )
        registry2 = Registry.objects.create(
            host=host2, name="registry2", serveraddress="http://localhost:8082"
        )

        image1 = Image.objects.create(host=host1, name="image1", registry=registry1)
        image2 = Image.objects.create(host=host2, name="image2", registry=registry2)

        network1 = Network.objects.create(host=host1, name="network1")
        network2 = Network.objects.create(host=host2, name="network2")

        volume1 = Volume.objects.create(host=host1, name="volume1")
        volume2 = Volume.objects.create(host=host1, name="volume2")
        volume3 = Volume.objects.create(host=host2, name="volume3")

        Container.objects.create(
            host=host1,
            image=image1,
            name="container1",
            operation="none",
            state="created",
            ContainerID="1234",
        )
        Container.objects.create(
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

        cls.create_data = [
            {
                "host": host1.pk,
                "image": image1.pk,
                "name": "container5",
                "ports": [
                    {"public_port": 80, "private_port": 80, "type": "tcp"},
                    {"public_port": 443, "private_port": 443, "type": "tcp"},
                ],
                "env": [
                    {"var_name": "ENV", "value": "prod"},
                    {"var_name": "CONFIG_FILE", "value": "/etc/my_config.json"},
                ],
                "labels": [
                    {"key": "truc.muche.com", "value": "something"},
                    {"key": "bidule.somewhere", "value": "super"},
                ],
                "mounts": [
                    {"source": "/data", "volume": volume1.pk},
                    {"source": "/etc", "volume": volume2.pk},
                ],
                "binds": [
                    {"host_path": "/opt/ct5/data", "container_path": "/data"},
                ],
                "network_settings": [
                    {"network": network1.pk},
                ],
                "devices": [
                    {"host_path": "/dev/sda", "container_path": "/dev/xvdc"},
                ]
            },
            {
                "host": host2.pk,
                "image": image2.pk,
                "name": "container6",
                "network_settings": [
                    {"network": network2.pk},
                ],
            },
            {
                "host": host2.pk,
                "image": image2.pk,
                "name": "container7",
                "network_settings": [
                    {"network": network2.pk},
                ],
            },
            {
                "host": host2.pk,
                "image": image2.pk,
                "name": "container8",
                "ports": [],
                "env": [],
                "labels": [],
                "mounts": [
                    {"source": "/data", "volume": volume3.pk},
                    {"source": "/etc", "volume": volume3.pk},
                ],
            },
            {
                "host": host2.pk,
                "image": image2.pk,
                "name": "container9",
                "ports": [],
                "env": [],
                "labels": [],
                "mounts": [
                    {"source": "/data", "volume": volume3.pk},
                    {"source": "/etc", "volume": volume3.pk},
                ],
            },
            {
                "host": host2.pk,
                "image": image2.pk,
                "name": "container10",
                "ports": [],
                "env": [{"var_name": "ENV", "value": ""}],
                "labels": [],
                "cap_add": ["NET_ADMIN"],
            },
        ]

    def test_that_patch_overwrites_data_only_when_explicitly_set(self):
        """Test that patch overwrites data only when explicitly set"""

        # Assign model-level permission
        obj_perm = ObjectPermission(
            name="Test permission", actions=["add", "change", "view"]
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))
        obj_perm.object_types.add(ObjectType.objects.get_for_model(Container))
        obj_perm.object_types.add(ObjectType.objects.get_for_model(Bind))
        obj_perm.object_types.add(ObjectType.objects.get_for_model(Env))

        host3 = Host.objects.create(
            endpoint="http://localhost:8080",
            name="host3",
        )
        registry3 = Registry.objects.create(
            host=host3,
            name="registry3",
            serveraddress="http://localhost:8080",
        )
        image3 = Image.objects.create(
            host=host3,
            name="image3",
            registry=registry3,
        )
        container11 = Container.objects.create(
            host=host3,
            image=image3,
            name="container11",
            operation="none",
            state="created",
        )
        Bind.objects.create(
            container=container11,
            host_path="/opt/ct11/data",
            container_path="/data",
        )
        Env.objects.create(
            container=container11,
            var_name="FOO",
            value="bar",
        )

        response = self.client.patch(
            reverse(f"plugins-api:{self._get_view_namespace()}:container-list"),
            [
                {
                    "id": container11.pk,
                    "host": host3.pk,
                    "image": image3.pk,
                    "name": "container11",
                    "binds": [],  # explicitly remove binds
                    # but don't specify envs to not overwrite them
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_200_OK)

        self.assertEqual(Bind.objects.filter(container=container11).count(), 0)
        self.assertEqual(Env.objects.filter(container=container11).count(), 1)

    def test_logs_endpoint(self):
        """Test logs endpoint"""

        container = Container.objects.get(name="container1")
        container_id = container.ContainerID

        endpoint = reverse(
            viewname=f"plugins-api:{self._get_view_namespace()}:container-logs",
            kwargs={"pk": container.pk},
        )

        # Add object-level permission
        obj_perm = ObjectPermission(
            name="Test permission",
            constraints={"pk": container.pk},
            actions=["view"],
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        with requests_mock.Mocker() as m:
            m.get(
                f"http://localhost:8080/api/engine/containers/{container_id}/logs",
                text="Hello > World",
            )

            response = self.client.get(endpoint, **self.header)
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(response.data, "Hello &gt; World")

    def test_that_container_host_cannot_be_changed(self):
        """Test that container's host cannot be changed"""

        host1 = Host.objects.create(name="host4")
        host2 = Host.objects.create(name="host5")

        registry1 = Registry.objects.create(
            host=host1, name="registry4", serveraddress="http://localhost:8080"
        )
        registry2 = Registry.objects.create(
            host=host2, name="registry5", serveraddress="http://localhost:8082"
        )

        image1 = Image.objects.create(host=host1, name="image", registry=registry1)
        image2 = Image.objects.create(host=host2, name="image", registry=registry2)

        container = Container.objects.create(host=host1, image=image1, name="container")

        obj_perm = ObjectPermission(name="Test permission", actions=["change"])
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        response = self.client.patch(
            reverse(f"plugins-api:{self._get_view_namespace()}:container-list"),
            [
                {
                    "id": container.pk,
                    "host": host2.pk,
                    "image": image2.pk,
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content, b'{"detail":"Cannot change the host\'s container"}'
        )
