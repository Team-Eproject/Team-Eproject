from django.urls import path
from .views import FoodListView, FoodCreateView
from .models import PreFood


app_name = "foods"

urlpatterns =  [
    path("", FoodListView.as_view()),
    path("entry/", FoodCreateView.as_view(), name="food-entry"),
]