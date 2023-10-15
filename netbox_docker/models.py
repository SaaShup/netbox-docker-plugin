"""Models definitions"""

from django.db import models
from django.urls import reverse
from django.core.validators import (
    URLValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from netbox.models import NetBoxModel


class Host(NetBoxModel):
    """Host definition class"""

    endpoint = models.CharField(max_length=1024, validators=[URLValidator()])
    name = models.CharField(
        unique=True,
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker:host", args=[self.pk])
