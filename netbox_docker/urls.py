"""URL definitions"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView
from . import models
from .views import (
    host as host_views,
    image as image_views,
    volume as volume_views,
    network as network_views,
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
        "hosts/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="host_changelog",
        kwargs={"model": models.Host},
    ),
    path(
        "hosts/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="host_journal",
        kwargs={"model": models.Host},
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
        kwargs={"model": models.Image},
    ),
    path(
        "images/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="image_journal",
        kwargs={"model": models.Image},
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
        kwargs={"model": models.Volume},
    ),
    path(
        "volumes/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="volume_journal",
        kwargs={"model": models.Volume},
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
        kwargs={"model": models.Network},
    ),
    path(
        "networks/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="network_journal",
        kwargs={"model": models.Network},
    ),
)
