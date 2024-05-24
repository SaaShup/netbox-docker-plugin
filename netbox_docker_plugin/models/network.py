"""Models definitions"""

from django.db import models
from django.urls import reverse
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)
from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel
from .host import Host


class NetworkDriverChoices(ChoiceSet):
    """Network driver choices definition class"""

    key = "Network.driver"

    DEFAULT_VALUE = "bridge"

    CHOICES = [
        (None, "null", "dark"),
        ("bridge", "Bridge", "blue"),
        ("host", "Host", "red"),
    ]


class NetworkStateChoices(ChoiceSet):
    """Network state choices definition class"""

    key = "Network.state"

    DEFAULT_VALUE = "creating"

    CHOICES = [
        ("creating", "Creating", "blue"),
        ("created", "Created", "green"),
    ]


class Network(NetBoxModel):
    """Network definition class"""

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="networks")
    name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=3),
            MaxLengthValidator(limit_value=255),
        ],
    )
    driver = models.CharField(
        max_length=32,
        choices=NetworkDriverChoices,
        default=NetworkDriverChoices.DEFAULT_VALUE,
        blank=True,
        null=True,
    )
    NetworkID = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=128),
        ],
        default=None,
        blank=True,
        null=True,
    )
    state = models.CharField(
        max_length=32,
        choices=NetworkStateChoices,
        default=NetworkStateChoices.DEFAULT_VALUE,
        blank=False,
        null=False,
    )

    class Meta:
        """Network Model Meta Class"""

        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=["host", "name"], name="%(app_label)s_%(class)s_unique_name_host"
            ),
            models.UniqueConstraint(
                fields=["host", "NetworkID"],
                name="%(app_label)s_%(class)s_unique_NetworkID_host",
            ),
        )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker_plugin:network", args=[self.pk])
