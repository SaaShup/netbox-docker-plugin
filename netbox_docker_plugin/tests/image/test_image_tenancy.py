"""Image ↔ Tenant / TenantGroup relationship tests."""

from django.test import TestCase

from tenancy.models import Tenant, TenantGroup

from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry


class ImageTenancyTestCase(TestCase):
    """Test the optional FK links between Image, Tenant and TenantGroup."""

    @classmethod
    def setUpTestData(cls):
        cls.host = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        cls.registry = Registry.objects.filter(name="dockerhub")[0]
        cls.tenant_group = TenantGroup(name="Group 1", slug="group-1")
        cls.tenant_group.save()
        cls.tenant = Tenant.objects.create(
            name="Tenant 1", slug="tenant-1", group=cls.tenant_group
        )

    def test_image_without_tenancy(self):
        """An Image with no tenant or group is valid."""
        image = Image.objects.create(
            name="img-no-tenant", host=self.host, registry=self.registry
        )
        self.assertIsNone(image.tenant)
        self.assertIsNone(image.tenant_group)

    def test_image_with_tenant(self):
        """An Image can be linked to a Tenant."""
        image = Image.objects.create(
            name="img-tenant",
            host=self.host,
            registry=self.registry,
            tenant=self.tenant,
        )
        image.refresh_from_db()
        self.assertEqual(image.tenant, self.tenant)

    def test_image_with_tenant_group(self):
        """An Image can be linked to a TenantGroup."""
        image = Image.objects.create(
            name="img-group",
            host=self.host,
            registry=self.registry,
            tenant_group=self.tenant_group,
        )
        image.refresh_from_db()
        self.assertEqual(image.tenant_group, self.tenant_group)

    def test_image_with_tenant_and_tenant_group(self):
        """An Image can be linked to both a Tenant and a TenantGroup simultaneously."""
        image = Image.objects.create(
            name="img-both",
            host=self.host,
            registry=self.registry,
            tenant=self.tenant,
            tenant_group=self.tenant_group,
        )
        image.refresh_from_db()
        self.assertEqual(image.tenant, self.tenant)
        self.assertEqual(image.tenant_group, self.tenant_group)

    def test_set_null_on_tenant_delete(self):
        """Deleting a Tenant sets the Image.tenant FK to NULL."""
        tenant = Tenant.objects.create(name="Tenant del", slug="tenant-del")
        image = Image.objects.create(
            name="img-tenant-del",
            host=self.host,
            registry=self.registry,
            tenant=tenant,
        )
        tenant.delete()
        image.refresh_from_db()
        self.assertIsNone(image.tenant)

    def test_set_null_on_tenant_group_delete(self):
        """Deleting a TenantGroup sets the Image.tenant_group FK to NULL."""
        group = TenantGroup(name="Group del", slug="group-del")
        group.save()
        image = Image.objects.create(
            name="img-group-del",
            host=self.host,
            registry=self.registry,
            tenant_group=group,
        )
        group.delete()
        image.refresh_from_db()
        self.assertIsNone(image.tenant_group)

    def test_unlink_tenant(self):
        """Setting tenant to None removes the link without deleting the Tenant."""
        image = Image.objects.create(
            name="img-unlink-tenant",
            host=self.host,
            registry=self.registry,
            tenant=self.tenant,
        )
        image.tenant = None
        image.save()
        image.refresh_from_db()
        self.assertIsNone(image.tenant)
        self.assertTrue(Tenant.objects.filter(pk=self.tenant.pk).exists())

    def test_unlink_tenant_group(self):
        """Setting tenant_group to None removes the link without deleting the TenantGroup."""
        image = Image.objects.create(
            name="img-unlink-group",
            host=self.host,
            registry=self.registry,
            tenant_group=self.tenant_group,
        )
        image.tenant_group = None
        image.save()
        image.refresh_from_db()
        self.assertIsNone(image.tenant_group)
        self.assertTrue(TenantGroup.objects.filter(pk=self.tenant_group.pk).exists())
