from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('upload', views.FileUploadViewSet, basename='upload')
router.register('files', views.FileViewSet)

urlpatterns = router.urls