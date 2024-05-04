""" Hooks on Django model signals. """

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from utilities.exceptions import AbortRequest

from .models import Container


@receiver(pre_delete, sender=Container)
def prevent_deleting_running_containers(instance, **_kwargs):
    """ Abort deletion if container is running. """

    if not instance.can_delete:
        raise AbortRequest(
            f"The container {instance.name} is running, please stop it before deletion"
        )
