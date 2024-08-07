""" Hooks on Django model signals. """

from django.db.models.signals import pre_delete, pre_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from utilities.exceptions import AbortRequest
from .models import Container


@receiver(pre_save, sender=Container)
def prevent_changing_container_host(instance, **_kwargs):
    """Prevent that a container's host cannot be changed"""

    if _kwargs.get("created") is not True:
        try:
            previous = Container.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            pass
        else:
            if previous.host.pk != instance.host.pk:
                raise AbortRequest("Cannot change the host's container")


@receiver(pre_delete, sender=Container)
def prevent_deleting_running_containers(instance, **_kwargs):
    """Abort deletion if container is running."""

    if not instance.can_delete:
        raise AbortRequest(
            f"The container {instance.name} is running, please stop it before deletion"
        )


@receiver(pre_save, sender=Container)
def restrict_container_actions(instance, **_kwargs):
    """Check if the container's state is correct for the given action"""

    if any(
        [
            instance.operation == "create" and not instance.can_create,
            instance.operation == "start" and not instance.can_start,
            instance.operation == "restart" and not instance.can_restart,
            instance.operation == "stop" and not instance.can_stop,
            instance.operation == "recreate" and not instance.can_recreate,
            instance.operation == "kill" and not instance.can_kill,
        ]
    ):
        raise AbortRequest(
            f"Cannot {instance.operation} container {instance.name} in state {instance.state}"
        )
