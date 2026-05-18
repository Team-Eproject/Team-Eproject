from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Food, PreFood
from .serializers import FoodSerializer, PreFoodSerializer

import json
from google.generativeai as genai

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators,csrf import csrf_exempt

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

def send_message(request):
    if request.method =='POST':
        genai.configure(api_key=GENERATIVE_AI_KEY)

        model = genai.GenerativeModel('gemini-pro')

        body = json.loads(request.body)

        request_data = body.get("request_data")

        prompt = f"""
        あなたは優秀な献立メニューアドバイザーです。

        データ:
        {request_data}
        """

        response = model.generate_content(prompt)

        return JsonResponse({
            "message": response.text
        })

    return JsonResponse({
        "error": "POST only"
    }, status=400)

