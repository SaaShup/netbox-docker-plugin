# pylint: disable=R0801
"""Container operation Views Test Case"""

from django.urls import reverse
from django.test import override_settings
from core.models import ObjectType
from core.models import ObjectChange
from core.choices import ObjectChangeActionChoices
from utilities.testing import ModelViewTestCase
from utilities.testing.utils import disable_warnings, post_data
from users.models import ObjectPermission
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.tests.base import BaseModelViewTestCase


class ContainerViewsTestCase(BaseModelViewTestCase, ModelViewTestCase):
    """Container operation Views Test Case Class"""

    model = Container

    def test_operation_start_object_without_permission(self):
        """Test operation start object without permission"""
        instance = self._get_queryset().exclude(state="running").first()

        # Try GET without permission
        with disable_warnings("django.request"):
            self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 403)

        # Try POST without permission
        request = {
            "path": reverse(
                "plugins:netbox_docker_plugin:container_operation",
                kwargs={"pk": instance.pk, "operation": "start"},
            ),
            "data": post_data({"operation": "start"}),
        }
        with disable_warnings("django.request"):
            self.assertHttpStatus(self.client.post(**request), 403)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_operation_start_object_with_permission(self):
        """Test operation start object with permission""" """  """
        instance = self._get_queryset().exclude(state="running").first()

        # Assign model-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["change"])
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        # Try GET with model-level permission
        self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 200)

        # Try POST with model-level permission
        request = {
            "path": reverse(
                "plugins:netbox_docker_plugin:container_operation",
                kwargs={"pk": instance.pk, "operation": "start"},
            ),
            "data": post_data({"operation": "start"}),
        }
        self.assertHttpStatus(self.client.post(**request), 302)
        instance = self._get_queryset().get(pk=instance.pk)
        self.assertInstanceEqual(instance, {"operation": "start"})

        objectchanges = ObjectChange.objects.filter(
            changed_object_type=ObjectType.objects.get_for_model(instance),
            changed_object_id=instance.pk,
        )
        self.assertEqual(len(objectchanges), 1)
        self.assertEqual(
            objectchanges[0].action, ObjectChangeActionChoices.ACTION_UPDATE
        )

    def test_operation_stop_object_without_permission(self):
        """Test operation stop object without permission"""
        instance = self._get_queryset().filter(state="running").first()

        # Try GET without permission
        with disable_warnings("django.request"):
            self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 403)

        # Try POST without permission
        request = {
            "path": reverse(
                "plugins:netbox_docker_plugin:container_operation",
                kwargs={"pk": instance.pk, "operation": "stop"},
            ),
            "data": post_data({"operation": "stop"}),
        }
        with disable_warnings("django.request"):
            self.assertHttpStatus(self.client.post(**request), 403)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_operation_stop_object_with_permission(self):
        """Test operation stop object with permission""" """  """
        instance = self._get_queryset().filter(state="running").first()

        # Assign model-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["change"])
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        # Try GET with model-level permission
        self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 200)

        # Try POST with model-level permission
        request = {
            "path": reverse(
                "plugins:netbox_docker_plugin:container_operation",
                kwargs={"pk": instance.pk, "operation": "stop"},
            ),
            "data": post_data({"operation": "stop"}),
        }
        self.assertHttpStatus(self.client.post(**request), 302)
        instance = self._get_queryset().get(pk=instance.pk)
        self.assertInstanceEqual(instance, {"operation": "stop"})

        objectchanges = ObjectChange.objects.filter(
            changed_object_type=ObjectType.objects.get_for_model(instance),
            changed_object_id=instance.pk,
        )
        self.assertEqual(len(objectchanges), 1)
        self.assertEqual(
            objectchanges[0].action, ObjectChangeActionChoices.ACTION_UPDATE
        )

    def test_operation_restart_object_without_permission(self):
        """Test operation restart object without permission"""
        instance = self._get_queryset().filter(state="running").first()

        # Try GET without permission
        with disable_warnings("django.request"):
            self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 403)

        # Try POST without permission
        request = {
            "path": reverse(
                "plugins:netbox_docker_plugin:container_operation",
                kwargs={"pk": instance.pk, "operation": "restart"},
            ),
            "data": post_data({"operation": "restart"}),
        }
        with disable_warnings("django.request"):
            self.assertHttpStatus(self.client.post(**request), 403)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_operation_restart_object_with_permission(self):
        """Test operation restart object with permission""" """  """
        instance = self._get_queryset().filter(state="running").first()

        # Assign model-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["change"])
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        # Try GET with model-level permission
        self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 200)

        # Try POST with model-level permission
        request = {
            "path": reverse(
                "plugins:netbox_docker_plugin:container_operation",
                kwargs={"pk": instance.pk, "operation": "restart"},
            ),
            "data": post_data({"operation": "restart"}),
        }
        self.assertHttpStatus(self.client.post(**request), 302)
        instance = self._get_queryset().get(pk=instance.pk)
        self.assertInstanceEqual(instance, {"operation": "restart"})

        objectchanges = ObjectChange.objects.filter(
            changed_object_type=ObjectType.objects.get_for_model(instance),
            changed_object_id=instance.pk,
        )
        self.assertEqual(len(objectchanges), 1)
        self.assertEqual(
            objectchanges[0].action, ObjectChangeActionChoices.ACTION_UPDATE
        )

    def test_operation_recreate_object_without_permission(self):
        """Test operation recreate object without permission"""
        instance = self._get_queryset().first()

        # Try GET without permission
        with disable_warnings("django.request"):
            self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 403)

        # Try POST without permission
        request = {
            "path": reverse(
                "plugins:netbox_docker_plugin:container_operation",
                kwargs={"pk": instance.pk, "operation": "recreate"},
            ),
            "data": post_data({"operation": "recreate"}),
        }
        with disable_warnings("django.request"):
            self.assertHttpStatus(self.client.post(**request), 403)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_operation_recreate_object_with_permission(self):
        """Test operation recreate object with permission""" """  """
        instance = self._get_queryset().first()

        # Assign model-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["change"])
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

        # Try GET with model-level permission
        self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 200)

        # Try POST with model-level permission
        request = {
            "path": reverse(
                "plugins:netbox_docker_plugin:container_operation",
                kwargs={"pk": instance.pk, "operation": "recreate"},
            ),
            "data": post_data({"operation": "recreate"}),
        }
        self.assertHttpStatus(self.client.post(**request), 302)
        instance = self._get_queryset().get(pk=instance.pk)
        self.assertInstanceEqual(instance, {"operation": "recreate"})

        objectchanges = ObjectChange.objects.filter(
            changed_object_type=ObjectType.objects.get_for_model(instance),
            changed_object_id=instance.pk,
        )
        self.assertEqual(len(objectchanges), 1)
        self.assertEqual(
            objectchanges[0].action, ObjectChangeActionChoices.ACTION_UPDATE
        )

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")

        registry1 = Registry.objects.create(
            host=host1, name="registry1", serveraddress="http://localhost:8080"
        )
        registry2 = Registry.objects.create(
            host=host2, name="registry2", serveraddress="http://localhost:8082"
        )

        image1 = Image.objects.create(host=host1, name="image1", registry=registry1)
        image2 = Image.objects.create(host=host2, name="image2", registry=registry2)

        Container.objects.create(
            host=host1,
            image=image1,
            name="container1",
            operation="none",
            state="created",
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
        Container.objects.create(
            host=host2,
            image=image2,
            name="container4",
            operation="none",
            state="running",
        )
