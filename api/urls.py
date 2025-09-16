from django.urls import path, include

from courses.views import (
    get_banners,
    get_notifications,
)


urlpatterns = [
    path("users/", include("users.urls")),
    path("courses/", include("courses.urls")),
    path("banners/", get_banners),
    path("notifications/", get_notifications),
]
