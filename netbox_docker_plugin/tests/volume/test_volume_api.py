"""Volume Test Case"""

from django.urls import reverse
from core.models import ObjectType
from rest_framework import status
from users.models import ObjectPermission
from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.volume import Volume
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.models.container import Container, Mount
from netbox_docker_plugin.tests.base import BaseAPITestCase


class VolumeApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Volume Test Case Class"""

    model = Volume
    brief_fields = ["display", "driver", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls) -> None:
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        Volume.objects.create(host=host1, name="volume1")
        Volume.objects.create(host=host1, name="volume2")
        Volume.objects.create(host=host2, name="volume3")

        cls.create_data = [
            {
                "host": host1.pk,
                "name": "volume4",
            },
            {
                "host": host1.pk,
                "name": "volume5",
            },
            {
                "host": host2.pk,
                "name": "volume6",
            },
        ]

    def test_that_embedded_anonymous_volume_is_created(self):
        """Test that embedded anonymous Volume is created on Container update"""

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
        obj_perm.object_types.add(ObjectType.objects.get_for_model(Mount))
        obj_perm.object_types.add(ObjectType.objects.get_for_model(Image))

        host = Host.objects.create(endpoint="http://localhost:8088", name="host8")

        registry = Registry.objects.create(
            host=host, name="registry8", serveraddress="http://localhost:8089"
        )

        image = Image.objects.create(host=host, name="image8", registry=registry)

        container = Container.objects.create(host=host, image=image, name="container8")

        response = self.client.patch(
            reverse(f"plugins-api:{self._get_view_namespace()}:container-list"),
            # pylint: disable=C0301
            [
                {
                    "id": container.pk,
                    "host": host.pk,
                    "mounts": [
                        {
                            "source": "/var/lib/docker/volumes/2419be4bd98f41a8e625c9e4479c1c5b0f8da4b5807f08a0340aa7a2e1574fdd/_data",
                            "volume": {
                                "name": "2419be4bd98f41a8e625c9e4479c1c5b0f8da4b5807f08a0340aa7a2e1574fdd",
                                "host": host.pk,
                            },
                        },
                        {
                            "source": "/var/lib/docker/volumes/844654ee4ac9d716679ed38b83c4ab6830a9db60ebf3fb2c000c7454bc41e9e2/_data",
                            "volume": {
                                "name": "844654ee4ac9d716679ed38b83c4ab6830a9db60ebf3fb2c000c7454bc41e9e2",
                                "host": host.pk,
                            },
                        },
                    ],
                }
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_200_OK)

        self.assertTrue(
            Volume.objects.filter(
                name="2419be4bd98f41a8e625c9e4479c1c5b0f8da4b5807f08a0340aa7a2e1574fdd",
                host=host.pk,
            ).exists()
        )

        self.assertTrue(
            Volume.objects.filter(
                name="844654ee4ac9d716679ed38b83c4ab6830a9db60ebf3fb2c000c7454bc41e9e2",
                host=host.pk,
            ).exists()
        )
