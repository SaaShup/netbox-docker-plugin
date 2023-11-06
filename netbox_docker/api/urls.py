"""API URLs definition"""

from netbox.api.routers import NetBoxRouter
from . import views


APP_NAME = "netbox_docker"

router = NetBoxRouter()
router.register("hosts", views.HostViewSet)
router.register("images", views.ImageViewSet)
router.register("volumes", views.VolumeViewSet)

urlpatterns = router.urls
