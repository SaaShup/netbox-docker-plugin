"""Image Test Case"""

import requests_mock
from django.urls import reverse
from core.models import ObjectType
from rest_framework import status
from users.models import ObjectPermission
from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.tests.base import BaseAPITestCase


class ImageApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Image Test Case Class"""

    model = Image
    brief_fields = [
        "Digest",
        "ImageID",
        "display",
        "id",
        "name",
        "size",
        "url",
        "version",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        registry = Registry.objects.filter(name="dockerhub")[0]

        Image.objects.create(host=host1, name="image1", registry=registry)
        Image.objects.create(host=host1, name="image2", registry=registry)
        Image.objects.create(
            host=host2,
            name="image3",
            ImageID="sha256:593aee2afb642798b83a85306d2625fd7f089c0a1242c7e75a237846d80aa2a0",
            registry=registry,
        )

        cls.create_data = [
            {
                "host": host1.pk,
                "name": "image4",
                "registry": registry.pk,
            },
            {
                "host": host1.pk,
                "name": "image5",
                "registry": registry.pk,
            },
            {
                "host": host2.pk,
                "name": "image6",
                "version": "testtesttesttesttesttesttesttesttesttesttesttesttest"
                + "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttes"
                + "ttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestte"
                + "sttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt",
                "registry": registry.pk,
            },
        ]

    def test_force_pull_endpoint(self):
        """Test force pull endpoint"""

        image = Image.objects.get(name="image1")

        endpoint = reverse(
            viewname=f"plugins-api:{self._get_view_namespace()}:image-force-pull",
            kwargs={"pk": image.pk},
        )

        # Add object-level permission
        obj_perm = ObjectPermission(
            name="Test permission",
            constraints={"pk": image.pk},
            actions=["add"],
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        with requests_mock.Mocker() as m:
            m.post(
                "http://localhost:8080/api/engine/images",
                text="{}",
            )

            response = self.client.post(endpoint, **self.header)
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(response.data, {"success": True, "payload": {}})
