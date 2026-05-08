from django.contrib import admin
from django.urls import path, include
# HomeViewでエラーが出てたのでいったん外しました。

urlpatterns = [
    path("admin/", admin.site.urls),

    # 画面表示
    path("", include("web.urls")),

    # API
    path("api/users/", include("apps.users.urls")),
    path("api/foods/", include("apps.foods.urls")),
]