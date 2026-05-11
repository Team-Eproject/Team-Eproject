from django.views.generic import CreateView
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView
from .models import Food, Category
from .forms import FoodForm
from .serializers import FoodSerializer

class FoodListView(ListAPIView):
    queryset = Food.objects.select_related("category").all()
    serializer_class = FoodSerializer

class FoodCreateView(CreateView):
    model = Food
    form_class =FoodForm
    template_name = ".html"
    success_url = reverse_lazy("foods:entry")

    def form_valid(self, form):
        custom_category = form.cleaned_data.get("custom_category")

        if custom_category:
            category, created = Category.objects.get_or_create(
                name=custom_category
            )
            form.instance.category = category

        if form.cleaned_data.get("no_expiration"):
            form.instance.expiration_date = None

        return super().form_valid(form)