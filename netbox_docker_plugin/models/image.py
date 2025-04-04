from django.db import models
from django.urls import reverse
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.contrib.auth.models import User  # Importation du modèle User
from netbox.models import NetBoxModel
from .host import Host
from .registry import Registry


class Image(NetBoxModel):
    """Image definition class"""

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="images")
    registry = models.ForeignKey(
        Registry,
        on_delete=models.CASCADE,
        related_name="images",
    )
    user = models.ForeignKey(
        User,  # Ajout de la clé étrangère vers le modèle User
        on_delete=models.CASCADE,
        related_name="images",  # Vous pouvez ajuster le related_name si nécessaire
        null=True,  # Permettre à l'image de ne pas avoir d'utilisateur
        blank=True,  # Permettre à l'image de ne pas avoir d'utilisateur
    )
    name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    version = models.CharField(
        default="latest",
        max_length=256,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=256),
        ],
    )
    size = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(limit_value=0),
            MaxValueValidator(limit_value=4096),
        ],
    )
    ImageID = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=128),
        ],
        default=None,
        blank=True,
        null=True,
    )
    Digest = models.CharField(
        max_length=512,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=512),
        ],
        default=None,
        blank=True,
        null=True,
    )

    class Meta:
        """Image Model Meta Class"""

        ordering = ("name", "version")
        constraints = (
            models.UniqueConstraint(
                fields=["host", "registry", "name", "version"],
                name="%(app_label)s_%(class)s_unique_version_name_registry_host",
            ),
            models.UniqueConstraint(
                fields=["host", "ImageID"],
                name="%(app_label)s_%(class)s_unique_ImageID_host",
            ),
        )

    def __str__(self):
        return f"{self.name}:{self.version}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker_plugin:image", args=[self.pk])
