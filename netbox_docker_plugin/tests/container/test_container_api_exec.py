# pylint: disable=R0801
"""Container Test Case"""

import requests_mock
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from core.models import ObjectType
from rest_framework import status
from users.models import ObjectPermission
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.tests.base import BaseAPITestCase


class ContainerApiExecTestCase(BaseAPITestCase):
    """Container Exec Test Case Class"""

    model = Container

    def setUp(self):
        super().setUp()

        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")

        registry1 = Registry.objects.create(
            host=host1, name="registry1", serveraddress="http://localhost:8080"
        )

        image1 = Image.objects.create(host=host1, name="image1", registry=registry1)

        container = Container.objects.create(
            host=host1,
            image=image1,
            name="container1",
            operation="none",
            state="created",
            ContainerID="1234",
        )

        # Add object-level permission
        obj_perm = ObjectPermission(
            name="Test permission",
            constraints={"pk": container.pk},
            actions=["add"],
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        self.endpoint = reverse(
            viewname=f"plugins-api:{self._get_view_namespace()}:container-exec",
            kwargs={"pk": container.pk},
        )

    def test_that_exec_endpoint_works(self):
        """Test Exec endpoint"""

        with requests_mock.Mocker(json_encoder=DjangoJSONEncoder) as m:
            m.put(
                "http://localhost:8080/api/engine/containers/1234/exec",
                json={"stdout": "..."},
            )

            response = self.client.post(
                self.endpoint, **self.header, data={"cmd": ["ls"]}, format="json"
            )
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(response.data, {"stdout": "..."})

    def test_that_exec_endpoint_with_invalid_command_fail(self):
        """Test exec endpoinr with invalid command"""

        response = self.client.post(
            self.endpoint, **self.header, data={"command": ["ls"]}, format="json"
        )
        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)

    def test_that_exec_endpoint_fail_with_backend_error(self):
        """Test Exec endpoint"""

        with requests_mock.Mocker(json_encoder=DjangoJSONEncoder) as m:
            m.put(
                "http://localhost:8080/api/engine/containers/1234/exec",
                text="Error",
                status_code= 500
            )

            response = self.client.post(
                self.endpoint, **self.header, data={"cmd": ["ls"]}, format="json"
            )
            self.assertHttpStatus(response, status.HTTP_502_BAD_GATEWAY)
            self.assertEqual(response.data, 'Error')
