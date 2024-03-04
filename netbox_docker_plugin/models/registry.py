"""Registry Model definition"""

from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)
from django.urls import reverse
from netbox.models import NetBoxModel


class Registry(NetBoxModel):
    """Registry definition class"""

    name = models.CharField(
        unique=True,
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

    @classmethod
    def get_default_registry(cls):
        """Return the default Registry"""
        # pylint: disable=W0612
        registry, created = cls.objects.get_or_create(
            name="dockerhub",
            serveraddress="https://registry.hub.docker.com/v2/",
        )
        return registry.pk

    class Meta:
        """Registry Model Meta Class"""

        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker_plugin:registry", args=[self.pk])
