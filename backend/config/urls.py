from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),

    # API
    path("api/users/", include("apps.users.urls")),
    path("api/foods/", include("apps.foods.urls")),
    path("api/", include("apps.shopping_memos.urls")),
]

# 開発中用 画像表示
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)