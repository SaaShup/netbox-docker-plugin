"""Container deletion tests — journal entry cleanup"""

import time

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from extras.models import JournalEntry
from netbox_docker_plugin.models.container import Container
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image
from netbox_docker_plugin.models.registry import Registry


def _make_journal_entries(container, count):
    ct = ContentType.objects.get_for_model(Container)
    batch_size = 10000
    for start in range(0, count, batch_size):
        JournalEntry.objects.bulk_create(
            [
                JournalEntry(
                    assigned_object_type=ct,
                    assigned_object_id=container.pk,
                    created_by=None,
                    kind="info",
                    comments=f"entry {start + i}",
                )
                for i in range(min(batch_size, count - start))
            ]
        )


class ContainerDeleteJournalTestCase(TestCase):
    """Verify that container deletion cleans up journal entries in batches."""

    @classmethod
    def setUpTestData(cls):
        cls.host = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        cls.registry = Registry.objects.create(
            host=cls.host,
            name="registry1",
            serveraddress="http://localhost:8080",
        )
        cls.image = Image.objects.create(
            host=cls.host, name="image1", registry=cls.registry
        )

    def _make_container(self, name="container1", state="exited"):
        """Create and return a Container in the given state."""
        return Container.objects.create(
            host=self.host,
            image=self.image,
            name=name,
            operation="none",
            state=state,
        )

    def test_delete_container_with_no_journal_entries(self):
        """Container with no journal entries can be deleted without errors."""
        container = self._make_container()
        pk = container.pk
        t0 = time.monotonic()
        container.delete()
        print(
            f"Deleted container (0 journal entries) in {(time.monotonic() - t0) * 1000:.1f}ms"
        )

        self.assertFalse(Container.objects.filter(pk=pk).exists())

    def test_delete_container_removes_journal_entries(self):
        """Journal entries linked to the deleted container are removed."""
        container = self._make_container(name="container2")
        _make_journal_entries(container, 5)
        ct = ContentType.objects.get_for_model(Container)

        self.assertEqual(
            JournalEntry.objects.filter(
                assigned_object_type=ct, assigned_object_id=container.pk
            ).count(),
            5,
        )

        pk = container.pk
        t0 = time.monotonic()
        container.delete()
        print(
            f"Deleted container (5 journal entries) in {(time.monotonic() - t0) * 1000:.1f}ms"
        )

        self.assertFalse(Container.objects.filter(pk=pk).exists())
        self.assertEqual(
            JournalEntry.objects.filter(
                assigned_object_type=ct, assigned_object_id=pk
            ).count(),
            0,
        )

    def test_delete_container_removes_many_journal_entries(self):
        """Deletion removes all journal entries regardless of count."""
        container = self._make_container(name="container3")
        _make_journal_entries(container, 500000)
        ct = ContentType.objects.get_for_model(Container)

        pk = container.pk
        t0 = time.monotonic()
        container.delete()
        elapsed = (time.monotonic() - t0) * 1000
        print(f"Deleted container (500000 journal entries) in {elapsed:.1f}ms")

        self.assertFalse(Container.objects.filter(pk=pk).exists())
        self.assertEqual(
            JournalEntry.objects.filter(
                assigned_object_type=ct, assigned_object_id=pk
            ).count(),
            0,
        )

    def test_delete_does_not_remove_journal_entries_of_other_containers(self):
        """Deleting one container must not remove journal entries of another."""
        container_a = self._make_container(name="container4a")
        container_b = self._make_container(name="container4b")
        _make_journal_entries(container_a, 3)
        _make_journal_entries(container_b, 3)
        ct = ContentType.objects.get_for_model(Container)

        t0 = time.monotonic()
        container_a.delete()
        print(
            f"Deleted container (3 journal entries) in {(time.monotonic() - t0) * 1000:.1f}ms"
        )

        self.assertEqual(
            JournalEntry.objects.filter(
                assigned_object_type=ct, assigned_object_id=container_b.pk
            ).count(),
            3,
        )
