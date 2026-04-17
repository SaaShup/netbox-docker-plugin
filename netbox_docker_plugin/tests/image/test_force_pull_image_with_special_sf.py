"""Test force pull image with special custom fields."""

import datetime
import requests_mock
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from users.models import ObjectPermission
from extras.models import CustomField
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.tests.base import BaseAPITestCase

class ForcePullImageWithSpecialCFTestCase(BaseAPITestCase):
    """Force Pull Image With Special Custom Fields Test Case Class """

    model = Image

    """Set up test data method."""
    @classmethod
    def setUpTestData(cls):
        # --- Create a host ---
        cls.host = Host.objects.create(endpoint="http://localhost:8080", name="host1")

        # --- Create a registry ---
        cls.registry = Registry.objects.filter(name="dockerhub")[0]

        # --- Create custom fields for Image ---
        ot = ContentType.objects.get_for_model(Image)

        cls.cf_date = CustomField.objects.create(
            name="cf_date",
            type="date",
            object_type=ot
        )
        cls.cf_date.save()

        cls.cf_datetime = CustomField.objects.create(
            name="cf_datetime",
            type="datetime",
            object_type=ot
        )
        cls.cf_datetime.save()

        # --- Create images ---
        Image.objects.create(
            host=cls.host,
            name="image_date",
            registry=cls.registry,
            custom_field_data={"cf_date": datetime.date.today()}
        )

        Image.objects.create(
            host=cls.host,
            name="image_datetime",
            registry=cls.registry,
            custom_field_data={"cf_datetime": datetime.datetime.now()}
        )

    def _add_object_permission(self, image):
        # --- Add object-level permission ---
        obj_perm = ObjectPermission(
            name="Test permission",
            constraints={"pk": image.pk},
            actions=["add"],
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ContentType.objects.get_for_model(self.model))

    def _force_pull_image(self, image):
        # --- Call add object-level permission ---
        self._add_object_permission(image)
        # --- Build image force pull API url ---
        endpoint = reverse(
            viewname=f"plugins-api:{self._get_view_namespace()}:image-force-pull",
            kwargs={"pk": image.pk},
        )
        with requests_mock.Mocker() as m:
            # --- Call API endpoint ---
            m.post(
                "http://localhost:8080/api/engine/images",
                text="{}",
            )
            response = self.client.post(endpoint, **self.header)
            return response

    def test_force_pull_with_date_custom_field(self):
        """Test force pull image with custom field of type Date."""
        image_date = Image.objects.get(name="image_date")
        response = self._force_pull_image(image_date)
        self.assertHttpStatus(response, status.HTTP_200_OK)
        self.assertEqual(response.data, {"success": True, "payload": {}})

    def test_force_pull_with_datetime_custom_field(self):
        """Test force pull image with custom field of type DateTime."""
        image_datetime = Image.objects.get(name="image_datetime")
        response = self._force_pull_image(image_datetime)
        self.assertHttpStatus(response, status.HTTP_200_OK)
        self.assertEqual(response.data, {"success": True, "payload": {}})
