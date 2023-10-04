"""API URLs definition"""

from netbox.api.routers import NetBoxRouter
from netbox_saashup.api import views

APP_NAME = "netbox_saashup"

router = NetBoxRouter()
router.register("engine", views.EngineViewSet)

urlpatterns = router.urls
