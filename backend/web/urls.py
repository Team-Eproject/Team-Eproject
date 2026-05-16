from django.urls import path
from . import views

urlpatterns = [
    path("", views.top, name="top"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("main/", views.main, name="main"),
]