"""URL definitions"""

from django.urls import path
from netbox_saashup import views, models
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView


urlpatterns = (
    # Mapping
    path("engines/", views.EngineListView.as_view(), name="engine_list"),
    path("engines/add/", views.EngineEditView.as_view(), name="engine_add"),
    path("engines/import/", views.EngineBulkImportView.as_view(), name="engine_import"),
)
