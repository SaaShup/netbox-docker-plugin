"""Host API Test Case"""

from core.models import ObjectType
from core.choices import ObjectChangeActionChoices
from core.models import ObjectChange
from users.models import ObjectPermission
from rest_framework import status
from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.registry import Registry
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
        "operation",
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

    def test_create_object(self):
        """
        POST a single object with permission.
        """
        # Add object-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["add"])
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        initial_count = self._get_queryset().count()
        response = self.client.post(
            self._get_list_url(), self.create_data[0], format="json", **self.header
        )
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        self.assertEqual(self._get_queryset().count(), initial_count + 1)
        instance = self._get_queryset().get(pk=response.data["id"])
        self.assertInstanceEqual(
            instance,
            self.create_data[0],
            exclude=self.validation_excluded_fields,
            api=True,
        )

        # Verify ObjectChange creation
        if hasattr(self.model, "to_objectchange"):
            objectchanges = ObjectChange.objects.filter(
                changed_object_type=ObjectType.objects.get_for_model(instance),
                changed_object_id=instance.pk,
            )
            self.assertEqual(len(objectchanges), 1)
            self.assertEqual(
                objectchanges[0].action, ObjectChangeActionChoices.ACTION_CREATE
            )

        registries = Registry.objects.filter(host=instance.pk)
        self.assertEqual(len(registries), 1)

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
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        response = self.client.delete(url, **self.header)
        self.assertHttpStatus(response, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self._get_queryset().filter(pk=instance.pk).exists())

        objectchanges = ObjectChange.objects.filter(
            changed_object_type=ObjectType.objects.get_for_model(instance),
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
