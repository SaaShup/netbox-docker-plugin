"""Host ↔ VirtualMachine relationship tests"""

from django.db import IntegrityError, transaction
from django.test import TestCase

from virtualization.models import VirtualMachine

from netbox_docker_plugin.models.host import Host


class HostVirtualMachineTestCase(TestCase):
    """Test the optional OneToOne link between Host and VirtualMachine."""

    @classmethod
    def setUpTestData(cls):
        cls.vm1 = VirtualMachine.objects.create(name="vm1")
        cls.vm2 = VirtualMachine.objects.create(name="vm2")
        cls.host = Host.objects.create(
            endpoint="http://localhost:8080",
            name="host1",
        )

    def test_host_without_virtual_machine(self):
        """A Host with no VirtualMachine linked is valid."""
        host = Host.objects.create(endpoint="http://localhost:8081", name="host2")
        self.assertIsNone(host.virtual_machine)

    def test_host_with_virtual_machine(self):
        """A Host can be linked to a VirtualMachine."""
        self.host.virtual_machine = self.vm1
        self.host.save()
        self.host.refresh_from_db()
        self.assertEqual(self.host.virtual_machine, self.vm1)

    def test_one_to_one_constraint(self):
        """Two Hosts cannot share the same VirtualMachine."""
        Host.objects.create(
            endpoint="http://localhost:8082",
            name="host_a",
            virtual_machine=self.vm2,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Host.objects.create(
                    endpoint="http://localhost:8083",
                    name="host_b",
                    virtual_machine=self.vm2,
                )

    def test_virtual_machine_set_null_on_delete(self):
        """Deleting the VirtualMachine sets the Host FK to NULL (SET_NULL)."""
        vm = VirtualMachine.objects.create(name="vm_to_delete")
        host = Host.objects.create(
            endpoint="http://localhost:8084",
            name="host_set_null",
            virtual_machine=vm,
        )
        vm.delete()
        host.refresh_from_db()
        self.assertIsNone(host.virtual_machine)

    def test_unlink_virtual_machine(self):
        """Setting virtual_machine to None removes the link without deleting either object."""
        vm = VirtualMachine.objects.create(name="vm_unlink")
        host = Host.objects.create(
            endpoint="http://localhost:8085",
            name="host_unlink",
            virtual_machine=vm,
        )
        host.virtual_machine = None
        host.save()
        host.refresh_from_db()
        self.assertIsNone(host.virtual_machine)
        self.assertTrue(VirtualMachine.objects.filter(pk=vm.pk).exists())
