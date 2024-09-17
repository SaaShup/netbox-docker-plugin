"""Host Views Test Case"""

from core.models import ObjectType
from core.choices import ObjectChangeActionChoices
from core.models import ObjectChange
from django.core.exceptions import ObjectDoesNotExist
from users.models import ObjectPermission
from utilities.testing import ViewTestCases, post_data
from netbox_docker_plugin.models.host import Host
from ..base import BaseModelViewTestCase


class HostViewsTestCase(BaseModelViewTestCase, ViewTestCases.PrimaryObjectViewTestCase):
    """Host Views Test Case Class"""

    model = Host
    form_data = {
        "name": "host4",
        "endpoint": "http://localhost:8084",
    }
    csv_data = (
        "name,endpoint",
        "host5,http://localhost:8084",
        "host6,http://localhost:8084",
        "host7,http://localhost:8084",
    )
    bulk_edit_data = {"endpoint": "http://localhost:8083"}

    def setUp(self):
        super().setUp()
        self.client.defaults = {"HTTP_ORIGIN": "http://localhost:8080"}

    def test_delete_object_with_permission(self):
        instance = self._get_queryset().first()

        # Assign model-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["delete"])
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        # Try GET with model-level permission
        self.assertHttpStatus(self.client.get(self._get_url("delete", instance)), 200)

        # Try POST with model-level permission
        request = {
            "path": self._get_url("delete", instance),
            "data": post_data({"confirm": True}),
        }
        self.assertHttpStatus(self.client.post(**request), 302)
        with self.assertRaises(ObjectDoesNotExist):
            self._get_queryset().get(pk=instance.pk)

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
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")
        host3 = Host.objects.create(endpoint="http://localhost:8081", name="host3")

        cls.csv_update_data = (
            "id,endpoint",
            f"{host1.pk},http://localhost:8085",
            f"{host2.pk},http://localhost:8085",
            f"{host3.pk},http://localhost:8085",
        )
