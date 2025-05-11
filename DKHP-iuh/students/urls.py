from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, RegistrationViewSet
from . import views

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'registrations', RegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('course-registration/', views.course_registration, name='course_registration'),
] 