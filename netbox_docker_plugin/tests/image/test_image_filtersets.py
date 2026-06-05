"""Image filterset tests for tenant and tenant_group filters."""

from django.test import TestCase

from tenancy.models import Tenant, TenantGroup

from netbox_docker_plugin.filtersets import ImageFilterSet
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry


class ImageFilterSetTenancyTestCase(TestCase):
    """Test ImageFilterSet filtering by tenant and tenant_group."""

    queryset = Image.objects.all()
    filterset = ImageFilterSet

    @classmethod
    def setUpTestData(cls):
        host = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        registry = Registry.objects.filter(name="dockerhub")[0]

        tenant_groups = (
            TenantGroup(name="Tenant Group 1", slug="tenant-group-1"),
            TenantGroup(name="Tenant Group 2", slug="tenant-group-2"),
            TenantGroup(name="Tenant Group 3", slug="tenant-group-3"),
        )
        for tg in tenant_groups:
            tg.save()

        tenants = (
            Tenant(name="Tenant 1", slug="tenant-1", group=tenant_groups[0]),
            Tenant(name="Tenant 2", slug="tenant-2", group=tenant_groups[1]),
            Tenant(name="Tenant 3", slug="tenant-3", group=tenant_groups[2]),
        )
        Tenant.objects.bulk_create(tenants)

        unassigned_group = TenantGroup(name="Unassigned Group", slug="unassigned-group")
        unassigned_group.save()
        cls.unassigned_tenant = Tenant.objects.create(
            name="Unassigned Tenant", slug="unassigned-tenant"
        )

        Image.objects.create(
            name="image1", host=host, registry=registry,
            tenant=tenants[0], tenant_group=tenant_groups[0],
        )
        Image.objects.create(
            name="image2", host=host, registry=registry,
            tenant=tenants[1], tenant_group=tenant_groups[1],
        )
        Image.objects.create(
            name="image3", host=host, registry=registry,
            tenant=tenants[2], tenant_group=tenant_groups[2],
        )

    def test_filter_by_tenant_id(self):
        """Filter images by one or more tenant IDs."""
        tenants = Tenant.objects.all()[:2]
        params = {"tenant_id": [tenants[0].pk, tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filter_by_single_tenant_id(self):
        """Filter images by a single tenant ID returns exactly one result."""
        tenant = Tenant.objects.get(slug="tenant-1")
        params = {"tenant_id": [tenant.pk]}
        qs = self.filterset(params, self.queryset).qs
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().name, "image1")

    def test_filter_by_tenant_group_id(self):
        """Filter images by one or more tenant group IDs."""
        groups = TenantGroup.objects.all()[:2]
        params = {"tenant_group_id": [groups[0].pk, groups[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filter_by_single_tenant_group_id(self):
        """Filter images by a single tenant group ID returns exactly one result."""
        group = TenantGroup.objects.get(slug="tenant-group-2")
        params = {"tenant_group_id": [group.pk]}
        qs = self.filterset(params, self.queryset).qs
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().name, "image2")

    def test_filter_no_match(self):
        """Filtering by a tenant with no images assigned returns an empty queryset."""
        params = {"tenant_id": [self.unassigned_tenant.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
