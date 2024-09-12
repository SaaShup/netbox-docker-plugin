"""URL definitions"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView
from .models.host import Host
from .models.image import Image
from .models.volume import Volume
from .models.network import Network
from .models.container import Container
from .models.registry import Registry
from .views import (
    host as host_views,
    image as image_views,
    volume as volume_views,
    network as network_views,
    container as container_views,
    env as env_views,
    label as label_views,
    port as port_views,
    mount as mount_views,
    bind as bind_views,
    network_setting as network_setting_views,
    registry as registry_views,
    device as device_views,
)

urlpatterns = (
    # Host
    path("hosts/", host_views.HostListView.as_view(), name="host_list"),
    path("hosts/add/", host_views.HostEditView.as_view(), name="host_add"),
    path("hosts/import/", host_views.HostBulkImportView.as_view(), name="host_import"),
    path("hosts/edit/", host_views.HostBulkEditView.as_view(), name="host_bulk_edit"),
    path(
        "hosts/delete/",
        host_views.HostBulkDeleteView.as_view(),
        name="host_bulk_delete",
    ),
    path("hosts/<int:pk>/", host_views.HostView.as_view(), name="host"),
    path("hosts/<int:pk>/edit/", host_views.HostEditView.as_view(), name="host_edit"),
    path(
        "hosts/<int:pk>/delete/",
        host_views.HostDeleteView.as_view(),
        name="host_delete",
    ),
    path(
        "hosts/<int:pk>/operation/<str:operation>/",
        host_views.HostOperationView.as_view(),
        name="host_operation",
    ),
    path(
        "hosts/<int:pk>/graph/",
        host_views.HostGraphView.as_view(),
        name="host_graph",
    ),
    path(
        "hosts/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="host_changelog",
        kwargs={"model": Host},
    ),
    path(
        "hosts/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="host_journal",
        kwargs={"model": Host},
    ),
    # Image
    path("images/", image_views.ImageListView.as_view(), name="image_list"),
    path("images/add/", image_views.ImageEditView.as_view(), name="image_add"),
    path(
        "images/import/", image_views.ImageBulkImportView.as_view(), name="image_import"
    ),
    path(
        "images/edit/", image_views.ImageBulkEditView.as_view(), name="image_bulk_edit"
    ),
    path(
        "images/delete/",
        image_views.ImageBulkDeleteView.as_view(),
        name="image_bulk_delete",
    ),
    path("images/<int:pk>/", image_views.ImageView.as_view(), name="image"),
    path(
        "images/<int:pk>/edit/", image_views.ImageEditView.as_view(), name="image_edit"
    ),
    path(
        "images/<int:pk>/delete/",
        image_views.ImageDeleteView.as_view(),
        name="image_delete",
    ),
    path(
        "images/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="image_changelog",
        kwargs={"model": Image},
    ),
    path(
        "images/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="image_journal",
        kwargs={"model": Image},
    ),
    # Volume
    path("volumes/", volume_views.VolumeListView.as_view(), name="volume_list"),
    path("volumes/add/", volume_views.VolumeEditView.as_view(), name="volume_add"),
    path(
        "volumes/import/",
        volume_views.VolumeBulkImportView.as_view(),
        name="volume_import",
    ),
    path(
        "volumes/delete/",
        volume_views.VolumeBulkDeleteView.as_view(),
        name="volume_bulk_delete",
    ),
    path("volumes/<int:pk>/", volume_views.VolumeView.as_view(), name="volume"),
    path(
        "volumes/<int:pk>/edit/",
        volume_views.VolumeEditView.as_view(),
        name="volume_edit",
    ),
    path(
        "volumes/<int:pk>/delete/",
        volume_views.VolumeDeleteView.as_view(),
        name="volume_delete",
    ),
    path(
        "volumes/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="volume_changelog",
        kwargs={"model": Volume},
    ),
    path(
        "volumes/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="volume_journal",
        kwargs={"model": Volume},
    ),
    # Network
    path("networks/", network_views.NetworkListView.as_view(), name="network_list"),
    path("networks/add/", network_views.NetworkEditView.as_view(), name="network_add"),
    path(
        "networks/import/",
        network_views.NetworkBulkImportView.as_view(),
        name="network_import",
    ),
    path(
        "networks/edit/",
        network_views.NetworkBulkEditView.as_view(),
        name="network_bulk_edit",
    ),
    path(
        "networks/delete/",
        network_views.NetworkBulkDeleteView.as_view(),
        name="network_bulk_delete",
    ),
    path("networks/<int:pk>/", network_views.NetworkView.as_view(), name="network"),
    path(
        "networks/<int:pk>/edit/",
        network_views.NetworkEditView.as_view(),
        name="network_edit",
    ),
    path(
        "networks/<int:pk>/delete/",
        network_views.NetworkDeleteView.as_view(),
        name="network_delete",
    ),
    path(
        "networks/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="network_changelog",
        kwargs={"model": Network},
    ),
    path(
        "networks/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="network_journal",
        kwargs={"model": Network},
    ),
    # Container
    path(
        "containers/",
        container_views.ContainerListView.as_view(),
        name="container_list",
    ),
    path(
        "containers/add/",
        container_views.ContainerNewView.as_view(),
        name="container_add",
    ),
    path(
        "containers/import/",
        container_views.ContainerBulkImportView.as_view(),
        name="container_import",
    ),
    path(
        "containers/edit/",
        container_views.ContainerBulkEditView.as_view(),
        name="container_bulk_edit",
    ),
    path(
        "containers/delete/",
        container_views.ContainerBulkDeleteView.as_view(),
        name="container_bulk_delete",
    ),
    path(
        "containers/<int:pk>/",
        container_views.ContainerView.as_view(),
        name="container",
    ),
    path(
        "containers/<int:pk>/logs",
        container_views.ContainerLogsView.as_view(),
        name="container_logs",
    ),
    path(
        "containers/<int:pk>/exec",
        container_views.ContainerExecView.as_view(),
        name="container_exec",
    ),
    path(
        "containers/<int:pk>/edit/",
        container_views.ContainerEditView.as_view(),
        name="container_edit",
    ),
    path(
        "containers/<int:pk>/delete/",
        container_views.ContainerDeleteView.as_view(),
        name="container_delete",
    ),
    path(
        "containers/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="container_changelog",
        kwargs={"model": Container},
    ),
    path(
        "containers/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="container_journal",
        kwargs={"model": Container},
    ),
    path(
        "containers/<int:pk>/operation/<str:operation>/",
        container_views.ContainerOperationView.as_view(),
        name="container_operation",
    ),
    # Env
    path(
        "env/",
        env_views.EnvListView.as_view(),
        name="env_list",
    ),
    path(
        "env/add/",
        env_views.EnvEditView.as_view(),
        name="env_add",
    ),
    path(
        "env/<int:pk>/edit/",
        env_views.EnvEditView.as_view(),
        name="env_edit",
    ),
    path(
        "env/<int:pk>/delete/",
        env_views.EnvDeleteView.as_view(),
        name="env_delete",
    ),
    # Label
    path(
        "labels/",
        label_views.LabelListView.as_view(),
        name="label_list",
    ),
    path(
        "labels/add/",
        label_views.LabelEditView.as_view(),
        name="label_add",
    ),
    path(
        "labels/<int:pk>/edit/",
        label_views.LabelEditView.as_view(),
        name="label_edit",
    ),
    path(
        "labels/<int:pk>/delete/",
        label_views.LabelDeleteView.as_view(),
        name="label_delete",
    ),
    # Port
    path(
        "ports/",
        port_views.PortListView.as_view(),
        name="port_list",
    ),
    path(
        "ports/add/",
        port_views.PortEditView.as_view(),
        name="port_add",
    ),
    path(
        "ports/<int:pk>/edit/",
        port_views.PortEditView.as_view(),
        name="port_edit",
    ),
    path(
        "ports/<int:pk>/delete/",
        port_views.PortDeleteView.as_view(),
        name="port_delete",
    ),
    # Mount
    path(
        "mounts/",
        mount_views.MountListView.as_view(),
        name="mount_list",
    ),
    path(
        "mounts/add/",
        mount_views.MountEditView.as_view(),
        name="mount_add",
    ),
    path(
        "mounts/<int:pk>/edit/",
        mount_views.MountEditView.as_view(),
        name="mount_edit",
    ),
    path(
        "mounts/<int:pk>/delete/",
        mount_views.MountDeleteView.as_view(),
        name="mount_delete",
    ),
    # Bind
    path(
        "binds/",
        bind_views.BindListView.as_view(),
        name="bind_list",
    ),
    path(
        "binds/add/",
        bind_views.BindEditView.as_view(),
        name="bind_add",
    ),
    path(
        "binds/<int:pk>/edit/",
        bind_views.BindEditView.as_view(),
        name="bind_edit",
    ),
    path(
        "binds/<int:pk>/delete/",
        bind_views.BindDeleteView.as_view(),
        name="bind_delete",
    ),
    # NetworkSetting
    path(
        "network-settings/",
        network_setting_views.NetworkSettingListView.as_view(),
        name="networksetting_list",
    ),
    path(
        "network-settings/add/",
        network_setting_views.NetworkSettingEditView.as_view(),
        name="networksetting_add",
    ),
    path(
        "network-settings/<int:pk>/edit/",
        network_setting_views.NetworkSettingEditView.as_view(),
        name="networksetting_edit",
    ),
    path(
        "network-settings/<int:pk>/delete/",
        network_setting_views.NetworkSettingDeleteView.as_view(),
        name="networksetting_delete",
    ),
    # Registry
    path(
        "registries/",
        registry_views.RegistryListView.as_view(),
        name="registry_list",
    ),
    path(
        "registries/add/",
        registry_views.RegistryEditView.as_view(),
        name="registry_add",
    ),
    path(
        "registries/delete/",
        registry_views.RegistryBulkDeleteView.as_view(),
        name="registry_bulk_delete",
    ),
    path(
        "registries/<int:pk>/", registry_views.RegistryView.as_view(), name="registry"
    ),
    path(
        "registries/<int:pk>/edit/",
        registry_views.RegistryEditView.as_view(),
        name="registry_edit",
    ),
    path(
        "registries/<int:pk>/delete/",
        registry_views.RegistryDeleteView.as_view(),
        name="registry_delete",
    ),
    path(
        "registries/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="registry_changelog",
        kwargs={"model": Registry},
    ),
    path(
        "registries/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="registry_journal",
        kwargs={"model": Registry},
    ),
    # Device
    path(
        "devices/",
        device_views.DeviceListView.as_view(),
        name="device_list",
    ),
    path(
        "devices/add/",
        device_views.DeviceEditView.as_view(),
        name="device_add",
    ),
    path(
        "devices/<int:pk>/edit/",
        device_views.DeviceEditView.as_view(),
        name="device_edit",
    ),
    path(
        "devices/<int:pk>/delete/",
        device_views.DeviceDeleteView.as_view(),
        name="device_delete",
    ),
)
