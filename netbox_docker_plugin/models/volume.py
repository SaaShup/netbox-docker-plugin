"""Volume Models definitions"""

from django.db import models
from django.urls import reverse
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)
from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel
from .host import Host


class VolumeDriverChoices(ChoiceSet):
    """Volume driver choices definition class"""

    key = "Volume.driver"

    DEFAULT_VALUE = "local"

    CHOICES = [
        ("local", "local", "dark"),
    ]


class Volume(NetBoxModel):
    """Volume definition class"""

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="volumes")
    name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=3),
            MaxLengthValidator(limit_value=255),
        ],
    )
    max_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
    )
    driver = models.CharField(
        max_length=32,
        choices=VolumeDriverChoices,
        default=VolumeDriverChoices.DEFAULT_VALUE,
        blank=False,
    )

    class Meta:
        """Volume Model Meta Class"""

        unique_together = ["host", "name"]
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker_plugin:volume", args=[self.pk])
