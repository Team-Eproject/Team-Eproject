from django.urls import path
from . import views

urlpatterns = [
    path("", views.top, name="top"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("main/", views.main, name="main"),
]