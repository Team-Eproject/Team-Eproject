from django.urls import path
from .views import FoodListView, FoodCreateView, CategoryListView

urlpatterns =  [
    path("foods/", FoodListView.as_view()),
    path("foods/create/", FoodCreateView.as_view()),
    path("categories/", CategoryListView.as_view()),
]