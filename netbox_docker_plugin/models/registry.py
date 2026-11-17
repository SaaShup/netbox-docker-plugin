"""Registry Model definition"""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)
from django.urls import reverse
from netbox.models import NetBoxModel
from .host import Host

DEFAULT_REGISTRY_NAME = "dockerhub"
DEFAULT_REGISTRY_SERVERADDRESS = "https://registry.hub.docker.com/v2/"


@receiver(post_save, sender=Host)
def create_default_registry(sender, **kwargs):  # pylint: disable=W0613
    """Ensure the shared default registry exists on Host creation"""

    if kwargs.get("created") is True:
        Registry.objects.get_or_create(
            name=DEFAULT_REGISTRY_NAME,
            defaults={"serveraddress": DEFAULT_REGISTRY_SERVERADDRESS},
        )


class Registry(NetBoxModel):
    """Registry definition class, shared by all hosts"""

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    serveraddress = models.URLField()
    username = models.CharField(blank=True, null=True, max_length=2048)
    password = models.CharField(blank=True, null=True, max_length=512)
    email = models.EmailField(blank=True, null=True, max_length=512)

    class Meta:
        """Registry Model Meta Class"""

        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker_plugin:registry", args=[self.pk])
