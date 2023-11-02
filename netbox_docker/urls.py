"""URL definitions"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView
from netbox_docker import views, models


urlpatterns = (
    # Host
    path("hosts/", views.HostListView.as_view(), name="host_list"),
    path("hosts/add/", views.HostEditView.as_view(), name="host_add"),
    path("hosts/import/", views.HostBulkImportView.as_view(), name="host_import"),
    path("hosts/edit/", views.HostBulkEditView.as_view(), name="host_bulk_edit"),
    path("hosts/delete/", views.HostBulkDeleteView.as_view(), name="host_bulk_delete"),
    path("hosts/<int:pk>/", views.HostView.as_view(), name="host"),
    path("hosts/<int:pk>/edit/", views.HostEditView.as_view(), name="host_edit"),
    path("hosts/<int:pk>/delete/", views.HostDeleteView.as_view(), name="host_delete"),
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
    path("images/", views.ImageListView.as_view(), name="image_list"),
    path("images/add/", views.ImageEditView.as_view(), name="image_add"),
    path("images/import/", views.ImageBulkImportView.as_view(), name="image_import"),
    path("images/edit/", views.ImageBulkEditView.as_view(), name="image_bulk_edit"),
    path(
        "images/delete/", views.ImageBulkDeleteView.as_view(), name="image_bulk_delete"
    ),
    path("images/<int:pk>/", views.ImageView.as_view(), name="image"),
    path("images/<int:pk>/edit/", views.ImageEditView.as_view(), name="image_edit"),
    path(
        "images/<int:pk>/delete/", views.ImageDeleteView.as_view(), name="image_delete"
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
)
