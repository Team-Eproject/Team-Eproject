from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Food, PreFood
from .serializers import FoodSerializer, PreFoodSerializer
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FoodForm


class FoodListView(ListAPIView):
    queryset = Food.objects.select_related("category").all()
    serializer_class = FoodSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "name"]

class FoodCreateAPIView(CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class CategoryListView(ListAPIView):
    queryset = PreFood.objects.all()
    serializer_class = PreFoodSerializer

#HTMLフォーム
class FoodCreateView(CreateView):
    model = Food
    form_class =FoodForm
    template_name = "foods/food_form.html"
    success_url = reverse_lazy("foods:food-entry")

    def form_valid(self, form):
        custom_category = form.cleaned_data.get("custom_category")

        if custom_category:
            category, created = PreFood.objects.get_or_create(
                name=custom_category
            )
            form.instance.category = category

        if form.cleaned_data.get("no_expiration"):
            form.instance.expiration_date = None

        return super().form_valid(form)


def register_page(request):
    return render(request, "foods/register.html", using="django")
