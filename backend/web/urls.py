from django.urls import path
from . import views

urlpatterns = [
    path("", views.top, name="top"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("home/", views.home, name="home"),
    path("foods/", views.foodslist, name="foodslist"),
    path("foods/register/", views.food_register, name="food_register"),
    path("foods/pre/", views.pre_foodlist, name="pre_foodlist"),
    path("foods/favorites/", views.favorite_foodslist, name="favorite_foodslist"),
    path("foods/detail/<int:food_id>/", views.foodlist_detail, name="foodlist_detail"),
    path("foods/delete-expired/", views.delete_expired_foods, name="delete_expired_foods"),
    path("foods/delete/<int:food_id>/", views.delete_food, name="delete_food"),
    path("user-info/", views.user_info, name="user_info"),
    path("logout/", views.user_logout, name="logout"),
]