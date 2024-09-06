"""Container Models definitions"""

# pylint: disable=E1101

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from utilities.choices import ChoiceSet
from utilities.querysets import RestrictedQuerySet
from netbox.models import NetBoxModel
from .image import Image
from .host import Host, HostStateChoices
from .network import Network
from .volume import Volume


class ContainerStateChoices(ChoiceSet):
    """Container state choices definition class"""

    key = "Container.state"

    DEFAULT_VALUE = "none"

    CHOICES = [
        ("created", "Created", "dark"),
        ("restarting", "Restarting", "blue"),
        ("running", "Running", "blue"),
        ("paused", "Paused", "blue"),
        ("exited", "Exited", "blue"),
        ("dead", "Dead", "blue"),
        ("none", "None", "white"),
    ]


class ContainerOperationChoices(ChoiceSet):
    """Container operation choices definition class"""

    key = "Container.operation"

    DEFAULT_VALUE = "create"

    CHOICES = [
        ("create", "Create", "dark"),
        ("start", "Start", "blue"),
        ("restart", "Restart", "blue"),
        ("stop", "Stop", "blue"),
        ("recreate", "Recreate", "blue"),
        ("kill", "Kill", "red"),
        ("none", "None", "white"),
    ]


class ContainerRestartPolicyChoices(ChoiceSet):
    """Container restart policy choices definition class"""

    key = "Container.restart_policy"

    DEFAULT_VALUE = "no"

    CHOICES = [
        ("no", "no", "dark"),
        ("on-failure", "on-failure", "blue"),
        ("always", "always", "blue"),
        ("unless-stopped", "unless-stopped", "blue"),
    ]


class PortTypeChoices(ChoiceSet):
    """Port type choices definition class"""

    key = "Port.type"

    DEFAULT_VALUE = "tcp"

    CHOICES = [
        ("tcp", "TCP", "dark"),
        ("udp", "UDP", "blue"),
    ]


class ContainerCapAddChoices(ChoiceSet):
    """cap-add choices definition class"""

    key = "Container.cap_add"

    CHOICES = [
        ("NET_ADMIN", "NET_ADMIN"),
    ]


class Container(NetBoxModel):
    """Container definition class"""

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="containers")
    image = models.ForeignKey(
        Image, on_delete=models.RESTRICT, related_name="containers"
    )
    name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    state = models.CharField(
        max_length=32,
        choices=ContainerStateChoices,
        default=ContainerStateChoices.DEFAULT_VALUE,
    )
    status = models.CharField(max_length=1024, blank=True, null=True)
    ContainerID = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=128),
        ],
        default=None,
        blank=True,
        null=True,
    )
    operation = models.CharField(
        max_length=32,
        choices=ContainerOperationChoices,
        default=ContainerOperationChoices.DEFAULT_VALUE,
    )
    hostname = models.CharField(
        max_length=256,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=256),
        ],
        default=None,
        blank=True,
        null=True,
    )
    restart_policy = models.CharField(
        max_length=32,
        choices=ContainerRestartPolicyChoices,
        default=ContainerRestartPolicyChoices.DEFAULT_VALUE,
    )
    cap_add = ArrayField(
        models.CharField(
            max_length=32, blank=True, null=True, choices=ContainerCapAddChoices
        ),
        null=True,
        blank=True,
    )

    @property
    def can_create(self) -> bool:
        """Check if the container can be created"""
        return self.state == "none"

    @property
    def can_start(self) -> bool:
        """Check if the container can be started"""
        return self.state in ["created", "exited", "dead"]

    @property
    def can_stop(self) -> bool:
        """Check if the container can be stopped"""
        return self.state in ["running"]

    @property
    def can_restart(self) -> bool:
        """Check if the container can be restarted"""
        return self.state in ["running"]

    @property
    def can_recreate(self) -> bool:
        """Check if the container can be recreated"""
        return self.state in ["created", "running", "exited", "dead"]

    @property
    def can_delete(self) -> bool:
        """Check if the container can be deleted"""
        return self.host.state in [
            HostStateChoices.STATE_DELETED,
            HostStateChoices.STATE_REFRESHING,
        ] or self.state in [
            "created",
            "paused",
            "exited",
            "dead",
        ]

    @property
    def can_kill(self) -> bool:
        """Check if the container can be killed"""
        return self.state in ["created", "restarting", "running", "exited", "dead"]

    class Meta:
        """Image Model Meta Class"""

        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                Lower("name"), "host", name="%(app_label)s_%(class)s_unique_name_host"
            ),
            models.UniqueConstraint(
                fields=["host", "ContainerID"],
                name="%(app_label)s_%(class)s_unique_ContainerID_host",
            ),
        )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker_plugin:container", args=[self.pk])

    def clean(self):
        super().clean()

        if self.host != self.image.host:
            raise ValidationError(
                {"image": f"Image {self.image} does not belong to host {self.host}."}
            )


class Port(models.Model):
    """Container definition class"""

    objects = RestrictedQuerySet.as_manager()

    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="ports"
    )
    private_port = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=0),
            MaxValueValidator(limit_value=65535),
        ],
    )
    public_port = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=0),
            MaxValueValidator(limit_value=65535),
        ],
    )
    type = models.CharField(
        max_length=3,
        choices=PortTypeChoices,
        default=PortTypeChoices.DEFAULT_VALUE,
    )

    class Meta:
        """Port Model Meta Class"""

        ordering = ("container",)
        constraints = (
            models.UniqueConstraint(
                "private_port",
                "public_port",
                "type",
                "container",
                name="%(app_label)s_%(class)s_unique_private_port_public_port_type_container'",
            ),
        )

    def __str__(self):
        return f"{self.type} {self.public_port}:{self.private_port}"


class Label(models.Model):
    """Label definition class"""

    objects = RestrictedQuerySet.as_manager()

    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="labels"
    )
    key = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    value = models.CharField(
        max_length=4095,
        validators=[
            MaxLengthValidator(limit_value=4095),
        ],
        blank=True,
    )

    class Meta:
        """Label Model Meta Class"""

        ordering = ("container", "key")
        constraints = (
            models.UniqueConstraint(
                "key",
                "container",
                name="%(app_label)s_%(class)s_unique_key_container'",
            ),
        )

    def __str__(self):
        return f"{self.key}"


class Env(models.Model):
    """Env definition class"""

    objects = RestrictedQuerySet.as_manager()

    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="env"
    )
    var_name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    value = models.CharField(
        blank=True,
        max_length=4096,
        validators=[
            MaxLengthValidator(limit_value=4096),
        ],
    )

    class Meta:
        """Env Model Meta Class"""

        ordering = ("container", "var_name")
        constraints = (
            models.UniqueConstraint(
                "var_name",
                "container",
                name="%(app_label)s_%(class)s_unique_var_name_container'",
            ),
        )

    def __str__(self):
        return f"{self.var_name}"


class Mount(models.Model):
    """Mount definition class"""

    objects = RestrictedQuerySet.as_manager()

    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="mounts"
    )
    volume = models.ForeignKey(Volume, on_delete=models.RESTRICT, related_name="mounts")
    source = models.CharField(
        max_length=1024,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=1024),
        ],
    )
    read_only = models.BooleanField(
        default=False,
    )

    class Meta:
        """Mount Model Meta Class"""

        ordering = ("container", "source", "volume")
        constraints = (
            models.UniqueConstraint(
                fields=["container", "source", "volume"],
                name="%(app_label)s_%(class)s_unique_volume",
            ),
        )

    def __str__(self):
        return f"{self.source}:{self.volume.name}"

    def clean(self):
        super().clean()

        if self.container.host != self.volume.host:
            raise ValidationError(
                {
                    "volume": f"Volume {self.volume} does not belong to host {self.container.host}."
                }
            )


class Bind(models.Model):
    """Bind definition class"""

    objects = RestrictedQuerySet.as_manager()

    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="binds"
    )
    host_path = models.CharField(
        max_length=1024,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=1024),
        ],
    )
    container_path = models.CharField(
        max_length=1024,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=1024),
        ],
    )
    read_only = models.BooleanField(
        default=False,
    )

    class Meta:
        """Mount Model Meta Class"""

        ordering = ("container", "container_path", "host_path")
        constraints = (
            models.UniqueConstraint(
                fields=["container", "container_path", "host_path"],
                name="%(app_label)s_%(class)s_unique_bind",
            ),
        )

    def __str__(self):
        return f"{self.host_path}:{self.container_path}"


class NetworkSetting(models.Model):
    """NetworkSetting definition class"""

    objects = RestrictedQuerySet.as_manager()
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="network_settings"
    )
    network = models.ForeignKey(
        Network, on_delete=models.RESTRICT, related_name="network_settings"
    )

    class Meta:
        """NetworkSetting Model Meta Class"""

        ordering = ("container", "network")
        constraints = (
            models.UniqueConstraint(
                fields=["container", "network"],
                name="%(app_label)s_%(class)s_unique_container_network",
            ),
        )

    def __str__(self):
        return f"{self.container.name}_{self.network.name}"

    def clean(self):
        super().clean()

        if self.container.host != self.network.host:
            raise ValidationError(
                {
                    "network": f"Network {self.network} does not belong to host "
                    + f"{self.container.host}."
                }
            )


class Device(models.Model):
    """Device definition class"""

    objects = RestrictedQuerySet.as_manager()

    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="devices"
    )
    host_path = models.CharField(
        max_length=1024,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=1024),
        ],
    )
    container_path = models.CharField(
        max_length=1024,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=1024),
        ],
    )

    class Meta:
        """Device Model Meta Class"""

        ordering = ("container", "container_path", "host_path")
        constraints = (
            models.UniqueConstraint(
                fields=["container", "container_path", "host_path"],
                name="%(app_label)s_%(class)s_unique_device",
            ),
        )

    def __str__(self):
        return f"{self.host_path}:{self.container_path}"
