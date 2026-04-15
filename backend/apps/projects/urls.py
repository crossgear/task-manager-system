from rest_framework import routers
from .api import ProjectViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = router.urls