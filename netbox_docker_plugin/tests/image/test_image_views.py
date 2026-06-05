"""Image Views Test Case"""

from tenancy.models import Tenant, TenantGroup
from utilities.testing import ViewTestCases
from netbox_docker_plugin.tests.base import BaseModelViewTestCase
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry


class ImageViewsTestCase(
    BaseModelViewTestCase, ViewTestCases.PrimaryObjectViewTestCase
):
    """Image Views Test Case Class"""

    model = Image

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")
        host3 = Host.objects.create(endpoint="http://localhost:8081", name="host3")

        registry = Registry.objects.filter(name="dockerhub")[0]

        tenant_group = TenantGroup(name="Group 1", slug="group-1")
        tenant_group.save()
        tenant = Tenant.objects.create(
            name="Tenant 1", slug="tenant-1", group=tenant_group
        )

        image1 = Image.objects.create(name="image1", host=host1, registry=registry)
        image2 = Image.objects.create(name="image2", host=host2, registry=registry)
        image3 = Image.objects.create(name="image3", host=host3, registry=registry)

        cls.form_data = {
            "name": "image1",
            "version": "v1.2.3",
            "host": host1.pk,
            "registry": registry.pk,
            "tenant_group": tenant_group.pk,
            "tenant": tenant.pk,
        }

        cls.csv_data = (
            "name,version,registry,host",
            f"image4,latest,{registry.pk},{host1.pk}",
            f"image5,,{registry.pk},{host2.pk}",
            f"image6,v1.2.3,{registry.pk},{host3.pk}",
        )

        cls.bulk_edit_data = {
            "version": "v1.0.0",
            "tenant": tenant.pk,
        }

        cls.csv_update_data = (
            "id,version,registry",
            f"{image1.pk},latest,{registry.pk}",
            f"{image2.pk},,{registry.pk}",
            f"{image3.pk},v1.0.0,{registry.pk}",
        )
