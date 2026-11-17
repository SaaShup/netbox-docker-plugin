# pylint: disable=C0301
"""Registry API Test Case"""

from core.models import ObjectType
from users.models import ObjectPermission
from django.db.models import ProtectedError
from rest_framework import status
from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.models.host import Host
from ..base import BaseAPITestCase


class RegistryApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Registry API Test Case Class"""

    model = Registry
    brief_fields = [
        "display",
        "email",
        "id",
        "name",
        "password",
        "serveraddress",
        "url",
        "username",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        Registry.objects.create(
            serveraddress="http://localhost:8080", name="registry0"
        )
        Registry.objects.create(
            serveraddress="http://localhost:8081", name="registry1"
        )
        Registry.objects.create(
            serveraddress="http://localhost:8082", name="registry2"
        )

        cls.create_data = [
            {
                "name": "github",
                "serveraddress": "https://ghcr.io",
            },
            {
                "name": "gitlab",
                "serveraddress": "http://registry.example.com",
                "username": "test",
                "password": "goodpassword",
                "email": "test@example.com",
            },
            {
                "name": "another",
                "serveraddress": "http://registry.example.com",
                "username": "Lorem ipsum dolor sit amet nulla amet aliquip. Minim irure aute cillum laborum sunt eu in mollit esse dolor irure pariatur in. Laboris qui enim cupidatat anim velit elit fugiat laborum nulla voluptate duis. Anim esse aliquip esse culpa occaecat incididunt esse excepteur fugiat. Eu cupidatat reprehenderit anim consequat esse non Lorem sint magna consequat tempor incididunt sit dolore tempor in fugiat reprehenderit irure. Eu, consequat Lorem aute sunt aliquip ad qui.Sunt nisi pariatur aliquip occaecat laborum ex occaecat eu eiusmod incididunt eiusmod ullamco nulla velit id do sit cillum velit nostrud ut exercitation nisi. Et est anim, esse laboris sit esse pariatur do enim. Anim, mollit ex laborum aliqua. Velit nulla cillum culpa officia incididunt consequat ut eiusmod pariatur nostrud voluptate eu ea cupidatat, nisi ullamco nulla eu elit exercitation.Ipsum irure est adipisicing ea cillum ullamco incididunt ipsum eu cupidatat Lorem occaecat adipisicing Lorem cupidatat pariatur ad proident eiusmod nostrud. Dolor enim excepteur nostrud dolore magna cillum irure duis. Ullamco ut occaecat laborum, cupidatat aliquip ullamco consequat do est do nisi veniam do adipisicing.Quis commodo minim id exercitation ipsum excepteur. Voluptate et, reprehenderit veniam qui nisi exercitation aliqua cillum reprehenderit ad consequat. Veniam ex officia reprehenderit dolore pariatur nostrud veniam ipsum exercitation pariatur quis irure ad eu quis.Adipisicing in irure in deserunt do irure officia. Dolor consequat occaecat minim ad adipisicing culpa pariatur et minim tempor aute ut eu veniam incididunt ut dolor fugiat. Tempor amet ipsum exercitation magna deserunt nulla elit sunt do voluptate non enim aute quis nostrud dolor cillum ea sint. Duis nostrud in Lorem quis esse ex aliquip consectetur et. Ipsum reprehenderit id ea culpa tempor nostrud in esse commodo ullamco. Laborum aliquip id magna est nulla non sunt eiusmod dolor incididunt labore qui Lorem sunt magna ullamco enim sint minim adipisicing.Labore reprehenderit eiusmod iqzertyuiop",
                "password": "none",
                "email": "test@example.com",
            },
            {
                "name": "registry",
                "serveraddress": "http://localhost:1010",
            },
        ]

    def test_that_username_limit_is_checked(self):
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

        response = self.client.post(
            self._get_list_url(),
            {
                "name": "another",
                "serveraddress": "http://registry.example.com",
                "username": "Lorem   ipsum dolor sit amet nulla amet aliquip. Minim irure aute cillum laborum sunt eu in mollit esse dolor irure pariatur in. Laboris qui enim cupidatat anim velit elit fugiat laborum nulla voluptate duis. Anim esse aliquip esse culpa occaecat incididunt esse excepteur fugiat. Eu cupidatat reprehenderit anim consequat esse non Lorem sint magna consequat tempor incididunt sit dolore tempor in fugiat reprehenderit irure. Eu, consequat Lorem aute sunt aliquip ad qui.Sunt nisi pariatur aliquip occaecat laborum ex occaecat eu eiusmod incididunt eiusmod ullamco nulla velit id do sit cillum velit nostrud ut exercitation nisi. Et est anim, esse laboris sit esse pariatur do enim. Anim, mollit ex laborum aliqua. Velit nulla cillum culpa officia incididunt consequat ut eiusmod pariatur nostrud voluptate eu ea cupidatat, nisi ullamco nulla eu elit exercitation.Ipsum irure est adipisicing ea cillum ullamco incididunt ipsum eu cupidatat Lorem occaecat adipisicing Lorem cupidatat pariatur ad proident eiusmod nostrud. Dolor enim excepteur nostrud dolore magna cillum irure duis. Ullamco ut occaecat laborum, cupidatat aliquip ullamco consequat do est do nisi veniam do adipisicing.Quis commodo minim id exercitation ipsum excepteur. Voluptate et, reprehenderit veniam qui nisi exercitation aliqua cillum reprehenderit ad consequat. Veniam ex officia reprehenderit dolore pariatur nostrud veniam ipsum exercitation pariatur quis irure ad eu quis.Adipisicing in irure in deserunt do irure officia. Dolor consequat occaecat minim ad adipisicing culpa pariatur et minim tempor aute ut eu veniam incididunt ut dolor fugiat. Tempor amet ipsum exercitation magna deserunt nulla elit sunt do voluptate non enim aute quis nostrud dolor cillum ea sint. Duis nostrud in Lorem quis esse ex aliquip consectetur et. Ipsum reprehenderit id ea culpa tempor nostrud in esse commodo ullamco. Laborum aliquip id magna est nulla non sunt eiusmod dolor incididunt labore qui Lorem sunt magna ullamco enim sint minim adipisicing.Labore reprehenderit eiusmod iqzertyuiop",
                "password": "none",
                "email": "test@example.com",
            },
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content,
            b'{"username":["Ensure this field has no more than 2048 characters."]}',
        )


class SharedRegistryApiTestCase(BaseAPITestCase):
    """Registries are shared by all hosts"""

    model = Registry

    @classmethod
    def setUpTestData(cls) -> None:
        cls.host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        cls.host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")
        cls.registry = Registry.objects.create(
            name="ghcr.io",
            serveraddress="https://ghcr.io/v2/",
            username="user",
            password="secret",
        )
        Image.objects.create(host=cls.host1, name="app", registry=cls.registry)

    def test_default_registry_is_shared(self):
        """Only one dockerhub registry exists whatever the number of hosts"""
        self.assertEqual(Registry.objects.filter(name="dockerhub").count(), 1)

    def test_host_deletion_keeps_registries_and_credentials(self):
        """Deleting a host must not delete registries"""
        self.host1.delete()

        registry = Registry.objects.get(pk=self.registry.pk)
        self.assertEqual(registry.username, "user")
        self.assertEqual(registry.password, "secret")

    def test_registry_used_by_images_cannot_be_deleted(self):
        """A registry still referenced by images is protected"""
        with self.assertRaises(ProtectedError):
            self.registry.delete()

    def test_legacy_host_field_is_ignored(self):
        """Agents still send a host on registry creation"""
        self.add_permissions("netbox_docker_plugin.add_registry")

        response = self.client.post(
            self._get_list_url(),
            [{"host": self.host2.pk, "name": "quay.io", "serveraddress": "https://quay.io/v2/"}],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        self.assertTrue(Registry.objects.filter(name="quay.io").exists())

    def test_duplicate_name_is_rejected(self):
        """Registry names are unique across all hosts"""
        self.add_permissions("netbox_docker_plugin.add_registry")

        response = self.client.post(
            self._get_list_url(),
            {"name": "ghcr.io", "serveraddress": "https://ghcr.io/v2/"},
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)

    def test_legacy_host_id_filter_returns_all_registries(self):
        """Agents still filter registries by host_id, they must get all of them"""
        self.add_permissions("netbox_docker_plugin.view_registry")

        response = self.client.get(
            f"{self._get_list_url()}?host_id={self.host2.pk}", **self.header
        )

        self.assertHttpStatus(response, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Registry.objects.count())

    def test_used_by_host_id_filter(self):
        """Filter registries used by the images of a host"""
        self.add_permissions("netbox_docker_plugin.view_registry")

        response = self.client.get(
            f"{self._get_list_url()}?used_by_host_id={self.host1.pk}", **self.header
        )
        self.assertEqual(
            [registry["name"] for registry in response.data["results"]], ["ghcr.io"]
        )

        response = self.client.get(
            f"{self._get_list_url()}?used_by_host_id={self.host2.pk}", **self.header
        )
        self.assertEqual(response.data["count"], 0)
