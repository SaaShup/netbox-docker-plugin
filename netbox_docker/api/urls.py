"""API URLs definition"""

from netbox.api.routers import NetBoxRouter
from netbox_docker.api import views

APP_NAME = "netbox_docker"

router = NetBoxRouter()
router.register("host", views.HostViewSet)

urlpatterns = router.urls
