""" Hooks on Django model signals. """

from django.db.models.signals import pre_delete, pre_save
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


@receiver(pre_save, sender=Container)
def restrict_container_actions(instance, **_kwargs):
    """ Check if the container's state is correct for the given action """

    if any([
        instance.operation == "create" and not instance.can_create,
        instance.operation == "start" and not instance.can_start,
        instance.operation == "restart" and not instance.can_restart,
        instance.operation == "stop" and not instance.can_stop,
        instance.operation == "recreate" and not instance.can_recreate,
    ]):
        raise AbortRequest(
            f"Cannot {instance.operation} container {instance.name} in state {instance.state}"
        )
