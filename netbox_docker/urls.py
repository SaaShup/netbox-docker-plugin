"""URL definitions"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView
from netbox_docker import views, models


urlpatterns = (
    # Host
    path("hosts/", views.HostListView.as_view(), name="host_list"),
    path("hosts/add/", views.HostEditView.as_view(), name="host_add"),
    path("hosts/import/", views.HostBulkImportView.as_view(), name="host_import"),
    path('hosts/edit/', views.HostBulkEditView.as_view(), name='host_bulk_edit'),
    path('hosts/delete/', views.HostBulkDeleteView.as_view(), name='host_bulk_delete'),
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
)
