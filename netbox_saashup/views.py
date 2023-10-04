"""Model views definitions"""

from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from netbox_saashup import models


class EngineView(generic.ObjectView):
    """Engine view definition"""

    queryset = models.Engine.objects.all()


class EngineListView(generic.ObjectListView):
    """Engine list view definition"""

    queryset = models.Engine.objects.all()


class EngineEditView(generic.ObjectEditView):
    """Engine edition view definition"""

    queryset = models.Engine.objects.all()


class EngineBulkImportView(generic.BulkImportView):
    """Engine bulk import view definition"""

    queryset = models.Engine.objects.all()
