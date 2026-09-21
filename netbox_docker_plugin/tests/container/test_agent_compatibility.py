"""Agent compatibility regression tests.

Each test pins one payload shape that netbox-docker-agent >= 1.25 sends back to
NetBox and that plugin 3.3.0 rejected. See the migrations 0036 to 0038.
"""

from django.test import TestCase
from netbox_docker_plugin.models.container import Container, Env, Port
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry


class AgentCompatibilityTestCase(TestCase):
    """Agent Compatibility Test Case Class"""

    objects = {}

    @classmethod
    def setUpTestData(cls) -> None:
        cls.objects["host1"] = Host.objects.create(
            endpoint="http://localhost:8080", name="host1"
        )
        cls.objects["registry1"] = Registry.objects.create(
            host=cls.objects["host1"],
            name="registry1",
            serveraddress="http://localhost:8080",
        )
        cls.objects["image1"] = Image.objects.create(
            host=cls.objects["host1"],
            name="image1",
            registry=cls.objects["registry1"],
        )

    def _container(self, name, **kwargs):
        """Create a container on the shared fixture host"""

        container = Container.objects.create(
            host=self.objects["host1"],
            image=self.objects["image1"],
            name=name,
            operation="none",
            state="created",
            **kwargs,
        )
        container.full_clean()
        return container

    def test_docker_log_drivers_are_accepted(self):
        """The agent reports LogConfig.Type verbatim from the Docker daemon"""

        for index, driver in enumerate(
            ["json-file", "syslog", "journald", "local", "none"]
        ):
            container = self._container(f"container-log-{index}", log_driver=driver)
            self.assertEqual(container.log_driver, driver)

    def test_log_driver_may_be_empty(self):
        """A container created before any refresh has no log driver yet"""

        container = self._container("container-log-null")
        self.assertIsNone(container.log_driver)

    def test_unpublished_port_is_accepted(self):
        """The agent uses -1 for exposed but unpublished ports"""

        container = self._container("container-port")
        port = Port.objects.create(
            container=container,
            private_port=8080,
            public_port=-1,
            type="tcp",
        )
        port.full_clean()
        self.assertEqual(port.public_port, -1)

    def test_docker_capabilities_are_accepted(self):
        """The agent reports the container capabilities with CAP_ stripped"""

        container = self._container(
            "container-caps",
            cap_add=["CHOWN", "SETUID", "SYS_ADMIN", "MKNOD"],
        )
        self.assertEqual(len(container.cap_add), 4)

    def test_long_environment_value_is_accepted(self):
        """Inline configuration and certificates exceed the old 4096 ceiling"""

        container = self._container("container-env")
        env = Env.objects.create(
            container=container,
            var_name="BIG_VALUE",
            value="x" * 20000,
        )
        env.full_clean()
        self.assertEqual(len(env.value), 20000)
