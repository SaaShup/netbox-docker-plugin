"""API Serializer definitions"""

# pylint: disable=E1101

from rest_framework import serializers
from utilities.query import dict_to_filter_params
from users.models import Token
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models.host import Host
from ..models.image import Image
from ..models.volume import Volume
from ..models.network import Network
from ..models.container import (
    Container,
    Port,
    Env,
    Label,
    Mount,
    Bind,
    NetworkSetting,
    Device,
)
from ..models.registry import Registry


class NestedTokenSerializer(WritableNestedSerializer):
    """Nested Token Serializer class"""

    class Meta:
        """Nested Token Serializer Meta class"""
        model = Token
        fields = ["id", "url", "display_url", "display", "key", "write_enabled"]


class NestedHostSerializer(WritableNestedSerializer):
    """Nested Host Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:host-detail"
    )

    class Meta:
        """Nested Host Serializer Meta class"""

        model = Host
        fields = (
            "id",
            "url",
            "display",
            "endpoint",
            "name",
            "state",
            "agent_version",
            "docker_api_version",
            "operation",
        )


class NestedImageSerializer(WritableNestedSerializer):
    """Nested Image Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:image-detail"
    )

    class Meta:
        """Nested Image Serializer Meta class"""

        model = Image
        fields = (
            "id",
            "url",
            "display",
            "name",
            "version",
            "size",
            "ImageID",
            "Digest",
        )


class NestedVolumeSerializer(WritableNestedSerializer):
    """Nested Volume Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:volume-detail"
    )

    class Meta:
        """Nested Volume Serializer Meta class"""

        model = Volume
        fields = (
            "id",
            "url",
            "display",
            "name",
            "driver",
        )

    def to_internal_value(self, data):
        if data is None:
            return None

        if isinstance(data, dict):
            params = dict_to_filter_params(data)
            if Volume.objects.filter(**params).count() == 0:
                host = Host.objects.get(pk=params["host"])
                volume = Volume(host=host, name=params["name"])
                volume.save()
                return volume

        return super().to_internal_value(data)


class NestedNetworkSerializer(WritableNestedSerializer):
    """Nested Network Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:network-detail"
    )

    class Meta:
        """Nested Network Serializer Meta class"""

        model = Network
        fields = (
            "id",
            "url",
            "display",
            "name",
            "driver",
            "NetworkID",
            "state",
        )


class NestedContainerSerializer(WritableNestedSerializer):
    """Nested Container Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:container-detail"
    )

    class Meta:
        """Nested Container Serializer Meta class"""

        model = Container
        fields = (
            "id",
            "url",
            "display",
            "name",
            "ContainerID",
            "state",
            "status",
            "restart_policy",
            "operation",
            "hostname",
            "cap_add",
        )


class NestedMountSerializer(WritableNestedSerializer):
    """Nested Mount Serializer class"""

    class Meta:
        """Nested Mount Serializer Meta class"""

        model = Mount
        fields = (
            "id",
            "source",
            "read_only",
        )


class NestedNetworkSettingSerializer(WritableNestedSerializer):
    """Nested NetworkSetting Serializer class"""

    network = NestedNetworkSerializer()

    class Meta:
        """Nested NetworkSetting Serializer Meta class"""

        model = NetworkSetting
        fields = ("id", "network")


class NestedRegistrySerializer(WritableNestedSerializer):
    """Nested Registry Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:registry-detail"
    )

    class Meta:
        """Nested Registry Serializer Meta class"""

        model = Registry
        fields = (
            "id",
            "name",
            "url",
            "display",
            "serveraddress",
            "username",
            "password",
            "email",
        )


class ImageSerializer(NetBoxModelSerializer):
    """Image Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:image-detail"
    )
    host = NestedHostSerializer()
    containers = NestedContainerSerializer(many=True, read_only=True)
    registry = NestedRegistrySerializer()

    class Meta:
        """Image Serializer Meta class"""

        model = Image
        fields = (
            "id",
            "url",
            "display",
            "host",
            "name",
            "version",
            "registry",
            "size",
            "ImageID",
            "Digest",
            "custom_fields",
            "created",
            "last_updated",
            "containers",
            "tags",
        )
        brief_fields = NestedImageSerializer.Meta.fields


class VolumeSerializer(NetBoxModelSerializer):
    """Volume Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:volume-detail"
    )
    host = NestedHostSerializer()
    mounts = NestedMountSerializer(many=True, read_only=True)

    class Meta:
        """Volume Serializer Meta class"""

        model = Volume
        fields = (
            "id",
            "url",
            "display",
            "host",
            "name",
            "driver",
            "custom_fields",
            "created",
            "last_updated",
            "mounts",
            "tags",
        )
        brief_fields = NestedVolumeSerializer.Meta.fields


class NetworkSerializer(NetBoxModelSerializer):
    """Network Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:network-detail"
    )
    host = NestedHostSerializer()
    network_settings = NestedNetworkSettingSerializer(many=True, read_only=True)

    class Meta:
        """Network Serializer Meta class"""

        model = Network
        fields = (
            "id",
            "url",
            "display",
            "host",
            "name",
            "driver",
            "NetworkID",
            "state",
            "custom_fields",
            "created",
            "last_updated",
            "network_settings",
            "tags",
        )
        brief_fields = NestedNetworkSerializer.Meta.fields


class PortSerializer(serializers.ModelSerializer):
    """Container Port Serializer class"""

    class Meta:
        """Container Port Serializer Meta class"""

        model = Port
        fields = (
            "public_port",
            "private_port",
            "type",
        )


class EnvSerializer(serializers.ModelSerializer):
    """Container Env Serializer class"""

    class Meta:
        """Container Env Serializer Meta class"""

        model = Env
        fields = (
            "var_name",
            "value",
        )


class LabelSerializer(serializers.ModelSerializer):
    """Container Label Serializer class"""

    class Meta:
        """Container Label Serializer Meta class"""

        model = Label
        fields = (
            "key",
            "value",
        )


class MountSerializer(serializers.ModelSerializer):
    """Container Mount Serializer class"""

    volume = NestedVolumeSerializer()

    class Meta:
        """Container Mount Serializer Meta class"""

        model = Mount
        fields = (
            "source",
            "volume",
            "read_only",
        )


class BindSerializer(serializers.ModelSerializer):
    """Container Bind Serializer class"""

    class Meta:
        """Container Bind Serializer Meta class"""

        model = Bind
        fields = (
            "host_path",
            "container_path",
            "read_only",
        )


class NetworkSettingSerializer(serializers.ModelSerializer):
    """Container NetworkSetting Serializer class"""

    network = NestedNetworkSerializer()

    class Meta:
        """Container NetworkSetting Serializer Meta class"""

        model = NetworkSetting
        fields = ("network",)


class DeviceSerializer(serializers.ModelSerializer):
    """Container Device Serializer class"""

    class Meta:
        """Container Device Serializer Meta class"""

        model = Device
        fields = (
            "host_path",
            "container_path",
        )


class ContainerSerializer(NetBoxModelSerializer):
    """Container Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:container-detail"
    )
    host = NestedHostSerializer()
    image = NestedImageSerializer()
    ports = PortSerializer(many=True, required=False)
    env = EnvSerializer(many=True, required=False)
    labels = LabelSerializer(many=True, required=False)
    mounts = MountSerializer(many=True, required=False)
    binds = BindSerializer(many=True, required=False)
    network_settings = NetworkSettingSerializer(many=True, required=False)
    devices = DeviceSerializer(many=True, required=False)

    class Meta:
        """Container Serializer Meta class"""

        model = Container
        fields = (
            "id",
            "url",
            "display",
            "host",
            "image",
            "name",
            "state",
            "operation",
            "status",
            "ContainerID",
            "hostname",
            "restart_policy",
            "cap_add",
            "ports",
            "env",
            "labels",
            "mounts",
            "binds",
            "network_settings",
            "devices",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
        )
        brief_fields = NestedContainerSerializer.Meta.fields

    def validate(self, data):
        attrs = data.copy()
        attrs.pop("ports", None)
        attrs.pop("env", None)
        attrs.pop("labels", None)
        attrs.pop("mounts", None)
        attrs.pop("binds", None)
        attrs.pop("network_settings", None)
        attrs.pop("devices", None)

        super().validate(attrs)

        return data

    # pylint: disable=R0912
    def create(self, validated_data):
        ports_data = validated_data.pop("ports", None)
        env_data = validated_data.pop("env", None)
        labels_data = validated_data.pop("labels", None)
        mounts_data = validated_data.pop("mounts", None)
        binds_data = validated_data.pop("binds", None)
        network_settings_data = validated_data.pop("network_settings", None)
        devices_data = validated_data.pop("devices", None)

        container = super().create(validated_data)

        if ports_data is not None:
            for port in ports_data:
                Port.objects.create(container=container, **port)

        if env_data is not None:
            for env in env_data:
                Env.objects.create(container=container, **env)

        if labels_data is not None:
            for label in labels_data:
                Label.objects.create(container=container, **label)

        if mounts_data is not None:
            for mount in mounts_data:
                obj = Mount(container=container, **mount)
                obj.full_clean()
                obj.save()

        if binds_data is not None:
            for bind in binds_data:
                obj = Bind(container=container, **bind)
                obj.full_clean()
                obj.save()

        if network_settings_data is not None:
            for network_setting in network_settings_data:
                obj = NetworkSetting(container=container, **network_setting)
                obj.full_clean()
                obj.save()

        if devices_data is not None:
            for device in devices_data:
                obj = Device(container=container, **device)
                obj.full_clean()
                obj.save()

        return container

    # pylint: disable=R0912
    def update(self, instance, validated_data):
        ports_data = validated_data.pop("ports", None)
        env_data = validated_data.pop("env", None)
        labels_data = validated_data.pop("labels", None)
        mounts_data = validated_data.pop("mounts", None)
        binds_data = validated_data.pop("binds", None)
        network_settings_data = validated_data.pop("network_settings", None)
        devices_data = validated_data.pop("devices", None)

        container = super().update(instance, validated_data)

        if ports_data is not None:
            Port.objects.filter(container=container).delete()
            for port in ports_data:
                Port.objects.create(container=container, **port)

        if env_data is not None:
            Env.objects.filter(container=container).delete()
            for env in env_data:
                Env.objects.create(container=container, **env)

        if labels_data is not None:
            Label.objects.filter(container=container).delete()
            for label in labels_data:
                Label.objects.create(container=container, **label)

        if mounts_data is not None:
            Mount.objects.filter(container=container).delete()
            for mount in mounts_data:
                obj = Mount(container=container, **mount)
                obj.full_clean()
                obj.save()

        if binds_data is not None:
            Bind.objects.filter(container=container).delete()
            for bind in binds_data:
                obj = Bind(container=container, **bind)
                obj.full_clean()
                obj.save()

        if network_settings_data is not None:
            NetworkSetting.objects.filter(container=container).delete()
            for network_setting in network_settings_data:
                obj = NetworkSetting(container=container, **network_setting)
                obj.full_clean()
                obj.save()

        if devices_data is not None:
            Device.objects.filter(container=container).delete()
            for device in devices_data:
                obj = Device(container=container, **device)
                obj.full_clean()
                obj.save()

        return container


class RegistrySerializer(NetBoxModelSerializer):
    """Registry Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:registry-detail"
    )
    host = NestedHostSerializer()
    images = NestedImageSerializer(many=True, read_only=True)

    class Meta:
        """Registry Serializer Meta class"""

        model = Registry
        fields = (
            "id",
            "name",
            "url",
            "host",
            "display",
            "serveraddress",
            "username",
            "password",
            "email",
            "images",
        )
        brief_fields = NestedRegistrySerializer.Meta.fields


class HostSerializer(NetBoxModelSerializer):
    """Host Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:host-detail"
    )
    images = NestedImageSerializer(many=True, read_only=True)
    volumes = NestedVolumeSerializer(many=True, read_only=True)
    networks = NestedNetworkSerializer(many=True, read_only=True)
    containers = NestedContainerSerializer(many=True, read_only=True)
    registries = NestedRegistrySerializer(many=True, read_only=True)
    token = NestedTokenSerializer(read_only=True)

    class Meta:
        """Host Serializer Meta class"""

        model = Host
        fields = (
            "id",
            "url",
            "display",
            "endpoint",
            "name",
            "state",
            "token",
            "netbox_base_url",
            "agent_version",
            "docker_api_version",
            "operation",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
            "images",
            "volumes",
            "networks",
            "containers",
            "registries",
        )
        brief_fields = NestedHostSerializer.Meta.fields


class ContainerCommandSerializer(serializers.Serializer):
    """Container command Serializer class"""

    cmd = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
