"""API Serializer definitions"""

# pylint: disable=E1101

from rest_framework import serializers
from users.api.nested_serializers import NestedTokenSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models.host import Host
from ..models.image import Image
from ..models.volume import Volume
from ..models.network import Network
from ..models.container import Container, Port, Env, Label, Mount, NetworkSetting


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
            "provider",
            "size",
            "ImageID",
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
            "name",
            "ContainerID",
            "state",
            "status",
            "operation",
            "hostname",
        )


class NestedMountSerializer(WritableNestedSerializer):
    """Nested Mount Serializer class"""

    class Meta:
        """Nested Mount Serializer Meta class"""

        model = Mount
        fields = (
            "id",
            "source",
        )


class NestedNetworkSettingSerializer(WritableNestedSerializer):
    """Nested NetworkSetting Serializer class"""

    network = NestedNetworkSerializer()

    class Meta:
        """Nested NetworkSetting Serializer Meta class"""

        model = NetworkSetting
        fields = ("id", "network")


class ImageSerializer(NetBoxModelSerializer):
    """Image Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:image-detail"
    )
    host = NestedHostSerializer()
    containers = NestedContainerSerializer(many=True, read_only=True)

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
            "provider",
            "size",
            "ImageID",
            "custom_fields",
            "created",
            "last_updated",
            "containers",
            "tags",
        )


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
        )


class NetworkSettingSerializer(serializers.ModelSerializer):
    """Container NetworkSetting Serializer class"""

    network = NestedNetworkSerializer()

    class Meta:
        """Container NetworkSetting Serializer Meta class"""

        model = NetworkSetting
        fields = ("network",)


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
    network_settings = NetworkSettingSerializer(many=True, required=False)

    class Meta:
        """Container Serializer Meta class"""

        model = Container
        fields = (
            "id",
            "url",
            "host",
            "image",
            "name",
            "state",
            "operation",
            "status",
            "ContainerID",
            "hostname",
            "ports",
            "env",
            "labels",
            "mounts",
            "network_settings",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
        )

    def validate(self, data):
        attrs = data.copy()
        attrs.pop("ports", None)
        attrs.pop("env", None)
        attrs.pop("labels", None)
        attrs.pop("mounts", None)
        attrs.pop("network_settings", None)

        super().validate(attrs)

        return data

    def create(self, validated_data):
        ports_data = validated_data.pop("ports", None)
        env_data = validated_data.pop("env", None)
        labels_data = validated_data.pop("labels", None)
        mounts_data = validated_data.pop("mounts", None)
        network_settings_data = validated_data.pop("network_settings", None)

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

        if network_settings_data is not None:
            for network_setting in network_settings_data:
                obj = NetworkSetting(container=container, **network_setting)
                obj.full_clean()
                obj.save()

        return container

    def update(self, instance, validated_data):
        ports_data = validated_data.pop("ports", None)
        env_data = validated_data.pop("env", None)
        labels_data = validated_data.pop("labels", None)
        mounts_data = validated_data.pop("mounts", None)
        network_settings_data = validated_data.pop("network_settings", None)

        container = super().update(instance, validated_data)

        Port.objects.filter(container=container).delete()
        if ports_data is not None:
            for port in ports_data:
                Port.objects.create(container=container, **port)

        Env.objects.filter(container=container).delete()
        if env_data is not None:
            for env in env_data:
                Env.objects.create(container=container, **env)

        Label.objects.filter(container=container).delete()
        if labels_data is not None:
            for label in labels_data:
                Label.objects.create(container=container, **label)

        Mount.objects.filter(container=container).delete()
        if mounts_data is not None:
            for mount in mounts_data:
                obj = Mount(container=container, **mount)
                obj.full_clean()
                obj.save()

        NetworkSetting.objects.filter(container=container).delete()
        if network_settings_data is not None:
            for network_setting in network_settings_data:
                obj = NetworkSetting(container=container, **network_setting)
                obj.full_clean()
                obj.save()

        return container


class HostSerializer(NetBoxModelSerializer):
    """Host Serializer class"""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_docker_plugin-api:host-detail"
    )
    images = NestedImageSerializer(many=True, read_only=True)
    volumes = NestedVolumeSerializer(many=True, read_only=True)
    networks = NestedNetworkSerializer(many=True, read_only=True)
    containers = NestedContainerSerializer(many=True, read_only=True)
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
            "custom_fields",
            "created",
            "last_updated",
            "tags",
            "images",
            "volumes",
            "networks",
            "containers",
        )
