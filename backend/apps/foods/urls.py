from django.urls import path
from .views import FoodListView, FoodCreateView, CategoryListView



urlpatterns =  [
    path("foods/", FoodListView.as_view()),
    # path("foods/create/", FoodCreateAPIView.as_view()),
    path("foods/categories/", CategoryListView.as_view()),
    path("foods/entry/", FoodCreateView.as_view(), name="food-entry"),
    # path("register/", register_page),
    # 今回時間の関係でAPI方面は無しなのでコメントアウトします
    # path("generate/", ai_menu_process),
]