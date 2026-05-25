from django.urls import path
from .views import(
    FoodListView, 
    FoodCreateView, 
    CategoryListView, 
    FoodCreateAPIView, 
    register_page,
    ai_menu_process,
)    



urlpatterns =  [
    path("foods/", FoodListView.as_view()),
    path("foods/create/", FoodCreateAPIView.as_view()),
    path("foods/categories/", CategoryListView.as_view()),
    path("foods/entry/", FoodCreateView.as_view(), name="food-entry"),
    path("register/", register_page),
    path("recipe/", ai_menu_process, name="ai_menu_process"),
]