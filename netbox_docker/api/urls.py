"""API URLs definition"""

from netbox.api.routers import NetBoxRouter
from . import views


APP_NAME = "netbox_docker"

router = NetBoxRouter()
router.register("hosts", views.HostViewSet)
router.register("images", views.ImageViewSet)
router.register("volumes", views.VolumeViewSet)
router.register("networks", views.NetworkViewSet)
router.register("containers", views.ContainerViewSet)

urlpatterns = router.urls
