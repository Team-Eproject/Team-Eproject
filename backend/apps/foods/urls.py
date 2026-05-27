from django.urls import path
from .views import FoodListView, FoodCreateView, CategoryListView, generate_menu_view



urlpatterns =  [
    path("foods/", FoodListView.as_view()),
    # path("foods/create/", FoodCreateAPIView.as_view()),
    path("foods/categories/", CategoryListView.as_view()),
    path("foods/entry/", FoodCreateView.as_view(), name="food-entry"),
    # path("register/", register_page),
    path("generate/", generate_menu_view),
]