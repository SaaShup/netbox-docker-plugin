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


@receiver(post_save, sender=Host)
def create_default_registry(sender, **kwargs): # pylint: disable=W0613
    """Create default registry on Host creation"""

    if kwargs.get("created") is True:
        registry = Registry(
            host=kwargs.get("instance"),
            name="dockerhub",
            serveraddress="https://registry.hub.docker.com/v2/",
        )
        registry.save()


class Registry(NetBoxModel):
    """Registry definition class"""

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="registries")
    name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    serveraddress = models.URLField()
    username = models.CharField(blank=True, null=True, max_length=512)
    password = models.CharField(blank=True, null=True, max_length=512)
    email = models.EmailField(blank=True, null=True, max_length=512)

    class Meta:
        """Registry Model Meta Class"""

        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=["host", "name"],
                name="%(app_label)s_%(class)s_name_host",
            ),
        )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker_plugin:registry", args=[self.pk])
