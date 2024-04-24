from rest_framework.routers import SimpleRouter

from .views import CollectionViewSet, LinkViewSet

router = SimpleRouter()
router.register("collections", CollectionViewSet, basename="collections")
router.register("links", LinkViewSet, basename="links")
urlpatterns = router.urls

