from django.contrib import admin
from django.urls import path, include
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
# from .views import HomeView
# HomeViewでエラーが出てたのでいったん外しました。

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
    path("api/", include("apps.users.urls")),
    path("api/", include("apps.foods.urls")),
    path("api/users/", include("apps.users.urls")),

#新規登録ページの作成
    path('signup/', CreateView.as_view(
        template_name = '',
        form_class=UserCreationForm,
        success_url='/foods',
    ), name='signup'),

    # path('home/', HomeView.as_view(
    #     template_name='',
    # ),
    #  name='home'),


    # API
    path("api/users/", include("apps.users.urls")),
    path("api/foods/", include("apps.foods.urls")),
]
