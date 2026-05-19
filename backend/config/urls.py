from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),

    # API
    path("api/users/", include("apps.users.urls")),
    path("api/foods/", include("apps.foods.urls")),
]
