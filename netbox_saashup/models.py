"""Models definitions"""

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from netbox.models import NetBoxModel


class Engine(NetBoxModel):
    """Engine definition class"""

    domain = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=2),
            MaxLengthValidator(limit_value=255),
        ],
    )
    port = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=65535),
        ],
    )

    class Meta:
        unique_together = ["domain", "port"]
        ordering = ("domain",)

    def __str__(self):
        return f"{self.domain}:{self.port}"
