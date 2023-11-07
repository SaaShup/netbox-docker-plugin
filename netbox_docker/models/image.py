"""Image Models definitions"""

from django.db import models
from django.urls import reverse
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel
from .host import Host


class ImageProviderChoices(ChoiceSet):
    """ImageProvider choices definition class"""

    key = "Image.provider"

    DEFAULT_VALUE = "dockerhub"

    CHOICES = [
        ("dockerhub", "Docker Hub", "dark"),
        ("github", "GitHub", "blue"),
    ]


class Image(NetBoxModel):
    """Image definition class"""

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="images")
    name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    version = models.CharField(
        default="latest",
        max_length=32,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32),
        ],
    )
    provider = models.CharField(
        max_length=32,
        choices=ImageProviderChoices,
        default=ImageProviderChoices.DEFAULT_VALUE,
        blank=False,
    )
    size = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(limit_value=0),
            MaxValueValidator(limit_value=4096),
        ],
    )

    class Meta:
        """Image Model Meta Class"""

        unique_together = ["host", "name", "version"]
        ordering = ("name", "version")

    def __str__(self):
        return f"{self.name}:{self.version}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker:image", args=[self.pk])
