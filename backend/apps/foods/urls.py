from django.urls import path
from .views import FoodListView, FoodCreateView, CategoryListView, register_page

urlpatterns =  [
    path("foods/", FoodListView.as_view()),
    path("foods/create/", FoodCreateView.as_view()),
    path("categories/", CategoryListView.as_view()),
    path("register/", register_page),
]