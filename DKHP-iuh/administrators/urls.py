from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, AdministratorViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'administrators', AdministratorViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 