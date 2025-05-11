from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/students/', include('students.urls')),
    path('api/administrators/', include('administrators.urls')),
    path('api/scheduling/', include('scheduling.urls')),
    path('api/registrations/', include('registrations.urls')),
    path('api/notifications/', include('notifications.urls')),
] 