from django.urls import path
from .views import LoginView, FoodListView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("foods/", FoodListView.as_view()),
]