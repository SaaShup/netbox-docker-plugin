"""Host API Test Case"""

from django.contrib.contenttypes.models import ContentType
from extras.choices import ObjectChangeActionChoices
from extras.models import ObjectChange
from users.models import ObjectPermission
from rest_framework import status
from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.host import Host
from ..base import BaseAPITestCase


class HostApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Host API Test Case Class"""

    model = Host
    brief_fields = [
        "agent_version",
        "display",
        "docker_api_version",
        "endpoint",
        "id",
        "name",
        "state",
        "url",
    ]
    create_data = [
        {
            "endpoint": "http://localhost:8083",
            "name": "host4",
        },
        {
            "endpoint": "http://localhost:8084",
            "name": "host5",
        },
        {
            "endpoint": "http://localhost:8085",
            "name": "host6",
        },
    ]

    def setUp(self):
        super().setUp()
        self.header["HTTP_ORIGIN"] = "http://localhost:8080"

    def test_delete_object(self):
        """
        DELETE a single object identified by its numeric ID.
        """
        instance = self._get_queryset().first()
        url = self._get_detail_url(instance)

        # Add object-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["delete"])
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ContentType.objects.get_for_model(self.model))

        response = self.client.delete(url, **self.header)
        self.assertHttpStatus(response, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self._get_queryset().filter(pk=instance.pk).exists())

        objectchanges = ObjectChange.objects.filter(
            changed_object_type=ContentType.objects.get_for_model(instance),
            changed_object_id=instance.pk,
        )
        self.assertEqual(len(objectchanges), 2)
        self.assertEqual(
            objectchanges[0].action, ObjectChangeActionChoices.ACTION_DELETE
        )
        self.assertEqual(
            objectchanges[1].action, ObjectChangeActionChoices.ACTION_UPDATE
        )

    @classmethod
    def setUpTestData(cls) -> None:
        Host.objects.create(endpoint="http://localhost:8080", name="host1")
        Host.objects.create(endpoint="http://localhost:8081", name="host2")
        Host.objects.create(endpoint="http://localhost:8081", name="host3")
