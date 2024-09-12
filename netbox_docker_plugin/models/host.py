"""Host Models definitions"""

from django.db import models
from django.urls import reverse
from django.core.validators import (
    URLValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from utilities.choices import ChoiceSet
from users.models import Token
from netbox.models import NetBoxModel


class HostStateChoices(ChoiceSet):
    """Host state choices definition class"""

    key = "Host.state"

    STATE_CREATED = "created"
    STATE_DELETED = "deleted"
    STATE_RUNNING = "running"
    STATE_REFRESHING = "refreshing"

    CHOICES = [
        (STATE_CREATED, "Created", "dark"),
        (STATE_RUNNING, "Running", "blue"),
        (STATE_DELETED, "Deleted", "blue"),
        (STATE_REFRESHING, "Refreshing", "blue"),
    ]


class HostOperationChoices(ChoiceSet):
    """Host operation choices definition class"""

    key = "Host.operation"

    OPERATION_REFRESH = "refresh"
    OPERATION_NONE = "none"

    CHOICES = [
        (OPERATION_REFRESH, "Refresh", "blue"),
        (OPERATION_NONE, "None", "white"),
    ]


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
    state = models.CharField(
        max_length=32,
        choices=HostStateChoices,
        default=HostStateChoices.STATE_CREATED,
    )
    token = models.ForeignKey(Token, on_delete=models.SET_NULL, null=True, blank=True)
    netbox_base_url = models.CharField(
        max_length=1024,
        validators=[URLValidator()],
        null=True,
        blank=True,
    )
    agent_version = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    docker_api_version = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    operation = models.CharField(
        max_length=32,
        choices=HostOperationChoices,
        default=HostOperationChoices.OPERATION_NONE,
    )

    class Meta:
        """Host Model Meta Class"""

        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker_plugin:host", args=[self.pk])

    def delete(self, using=None, keep_parents=False):
        self.state = HostStateChoices.STATE_DELETED
        self.save()

        return super().delete(using, keep_parents)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.operation == HostOperationChoices.OPERATION_REFRESH:
            self.state = HostStateChoices.STATE_REFRESHING

        return super().save(force_insert, force_update, using, update_fields)
