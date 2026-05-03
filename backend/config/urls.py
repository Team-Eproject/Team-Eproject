from django.urls import path, include
from django.views.generic immport CreateView
from django.views.generic import CreateView
from .views import HomeView

urlpatterns = [
    path("api/users/", include("apps.users.urls")),

#新規登録ページの作成
    path('signup/', CreateView.as_view(
        template_name = '',
        form_class=UserCreationForm,
        success_url='/foods',
    ), name='signup'),

    path('home/' HomeView.as_view(
        template_name='',
    ),
     name='home'),
]