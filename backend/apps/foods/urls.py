from django.urls import path
from .views import FoodListView
from .views import FoodCreateView


app_name = "foods"

urlpatterns =  [
    path("foods/", FoodListView.as_view()),
    path("foods/entry/", FoodCreateView.as_view()),
]