from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Food, PreFood
from .serializers import FoodSerializer, PreFoodSerializer

class FoodListView(ListAPIView):
    queryset = Food.objects.select_related("category").all()
    serializer_class = FoodSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "name"]


class FoodCreateView(CreateAPIView)  :
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class CategoryListView(ListAPIView):
    queryset = PreFood.objects.all()
    serializer_class = PreFoodSerializer