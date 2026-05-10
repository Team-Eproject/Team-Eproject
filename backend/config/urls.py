from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
# from .views import HomeView
=======
# HomeViewでエラーが出てたのでいったん外しました。
>>>>>>> 18e27a8a3443da8a9e46d01aad93fb44879ce0b2

urlpatterns = [
    path("admin/", admin.site.urls),

<<<<<<< HEAD
    path("api/", include("apps.users.urls")),
    path("api/", include("apps.foods.urls")),
    path("api/users/", include("apps.users.urls")),

#新規登録ページの作成
    path('signup/', CreateView.as_view(
        template_name = '',
        form_class=UserCreationForm,
        success_url='/foods',
    ), name='signup'),

    path('home/', HomeView.as_view(
        template_name='',
    ),
     name='home'),

]
=======
    # 画面表示
    path("", include("web.urls")),

    # API
    path("api/users/", include("apps.users.urls")),
    path("api/foods/", include("apps.foods.urls")),
]
>>>>>>> 18e27a8a3443da8a9e46d01aad93fb44879ce0b2
