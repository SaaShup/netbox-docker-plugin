"""Container Test Case"""

from utilities.testing import APIViewTestCases
from netbox_docker.models.container import Container
from netbox_docker.models.host import Host
from netbox_docker.models.network import Network
from netbox_docker.models.image import Image
from netbox_docker.models.volume import Volume
from netbox_docker.tests.base import BaseAPITestCase


class ContainerApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Container Test Case Class"""

    model = Container
    brief_fields = ["ContainerID", "id", "name", "state", "status", "url"]
    validation_excluded_fields = [
        "ports",
        "env",
        "labels",
        "mounts",
        "network_settings",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        image1 = Image.objects.create(host=host1, name="image1")
        image2 = Image.objects.create(host=host2, name="image2")

        network1 = Network.objects.create(host=host1, name="network1")
        network2 = Network.objects.create(host=host2, name="network2")

        volume1 = Volume.objects.create(host=host1, name="volume1")
        volume2 = Volume.objects.create(host=host1, name="volume2")

        Container.objects.create(host=host1, image=image1, name="container1")
        Container.objects.create(host=host1, image=image1, name="container2")
        Container.objects.create(host=host2, image=image2, name="container3")

        cls.create_data = [
            {
                "host": host1.pk,
                "image": image1.pk,
                "name": "container5",
                "ports": [
                    {"public_port": 80, "private_port": 80, "type": "tcp"},
                    {"public_port": 443, "private_port": 443, "type": "tcp"},
                ],
                "env": [
                    {"var_name": "ENV", "value": "prod"},
                    {"var_name": "CONFIG_FILE", "value": "/etc/my_config.json"},
                ],
                "labels": [
                    {"key": "truc.muche.com", "value": "something"},
                    {"key": "bidule.somewhere", "value": "super"},
                ],
                "mounts": [
                    {"source": "/data", "volume": volume1.pk},
                    {"source": "/etc", "volume": volume2.pk},
                ],
                "network_settings": [
                    {"network": network1.pk},
                ],
            },
            {
                "host": host2.pk,
                "image": image2.pk,
                "name": "container6",
                "network_settings": [
                    {"network": network2.pk},
                ],
            },
            {
                "host": host2.pk,
                "image": image2.pk,
                "name": "container7",
                "network_settings": [
                    {"network": network2.pk},
                ],
            },
            {
                "host": host2.pk,
                "image": image2.pk,
                "name": "container8",
                "ports": [],
                "env": [],
                "labels": [],
                "mounts": [],
            },
        ]
