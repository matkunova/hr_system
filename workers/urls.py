from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkerViewSet, WorkerImportView

router = DefaultRouter()
router.register(r'workers', WorkerViewSet, basename='worker')

urlpatterns = [
    path('api/workers/import/', WorkerImportView.as_view(), name='worker-import'),
    path('api/', include(router.urls)),
]