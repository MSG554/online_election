from rest_framework.routers import DefaultRouter
from .views import ElectionViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'elections', ElectionViewSet, basename='election')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = router.urls
