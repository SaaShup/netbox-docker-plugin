"""Registry API Test Case"""

from core.models import ObjectType
from users.models import ObjectPermission
from rest_framework import status
from utilities.testing import APIViewTestCases
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
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        Registry.objects.create(
            host=host1, serveraddress="http://localhost:8080", name="registry0"
        )
        Registry.objects.create(
            host=host1, serveraddress="http://localhost:8081", name="registry1"
        )
        Registry.objects.create(
            host=host2, serveraddress="http://localhost:8082", name="registry2"
        )

        cls.create_data = [
            {
                "host": host1.pk,
                "name": "github",
                "serveraddress": "https://ghcr.io",
            },
            {
                "host": host2.pk,
                "name": "gitlab",
                "serveraddress": "http://registry.example.com",
                "username": "test",
                "password": "goodpassword",
                "email": "test@example.com",
            },
            {
                "host": host2.pk,
                "name": "another",
                "serveraddress": "http://registry.example.com",
                "username": "Lorem ipsum dolor sit amet nulla amet aliquip. Minim irure aute cillum laborum sunt eu in mollit esse dolor irure pariatur in. Laboris qui enim cupidatat anim velit elit fugiat laborum nulla voluptate duis. Anim esse aliquip esse culpa occaecat incididunt esse excepteur fugiat. Eu cupidatat reprehenderit anim consequat esse non Lorem sint magna consequat tempor incididunt sit dolore tempor in fugiat reprehenderit irure. Eu, consequat Lorem aute sunt aliquip ad qui.Sunt nisi pariatur aliquip occaecat laborum ex occaecat eu eiusmod incididunt eiusmod ullamco nulla velit id do sit cillum velit nostrud ut exercitation nisi. Et est anim, esse laboris sit esse pariatur do enim. Anim, mollit ex laborum aliqua. Velit nulla cillum culpa officia incididunt consequat ut eiusmod pariatur nostrud voluptate eu ea cupidatat, nisi ullamco nulla eu elit exercitation.Ipsum irure est adipisicing ea cillum ullamco incididunt ipsum eu cupidatat Lorem occaecat adipisicing Lorem cupidatat pariatur ad proident eiusmod nostrud. Dolor enim excepteur nostrud dolore magna cillum irure duis. Ullamco ut occaecat laborum, cupidatat aliquip ullamco consequat do est do nisi veniam do adipisicing.Quis commodo minim id exercitation ipsum excepteur. Voluptate et, reprehenderit veniam qui nisi exercitation aliqua cillum reprehenderit ad consequat. Veniam ex officia reprehenderit dolore pariatur nostrud veniam ipsum exercitation pariatur quis irure ad eu quis.Adipisicing in irure in deserunt do irure officia. Dolor consequat occaecat minim ad adipisicing culpa pariatur et minim tempor aute ut eu veniam incididunt ut dolor fugiat. Tempor amet ipsum exercitation magna deserunt nulla elit sunt do voluptate non enim aute quis nostrud dolor cillum ea sint. Duis nostrud in Lorem quis esse ex aliquip consectetur et. Ipsum reprehenderit id ea culpa tempor nostrud in esse commodo ullamco. Laborum aliquip id magna est nulla non sunt eiusmod dolor incididunt labore qui Lorem sunt magna ullamco enim sint minim adipisicing.Labore reprehenderit eiusmod iqzertyuiop",
                "password": "none",
                "email": "test@example.com",
            },
            {
                "host": host1.pk,
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

        host = Host.objects.create(endpoint="http://localhost:8080", name="host3")

        response = self.client.post(
            self._get_list_url(),
            {
                "host": host.pk,
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
