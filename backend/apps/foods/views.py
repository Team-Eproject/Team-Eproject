from django.shortcuts import render
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse_lazy
from .forms import FoodForm
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Food, PreFood, Message
from .serializers import FoodSerializer, PreFoodSerializer

import json
from google import genai
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .services import generate_menu

class FoodListView(ListAPIView):
    queryset = Food.objects.select_related("category").all()
    serializer_class = FoodSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "name"]

class FoodApiCreateView(CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryListView(ListAPIView):
    queryset = PreFood.objects.all()
    serializer_class = PreFoodSerializer

#AIテスト用
@csrf_exempt
@require_POST
def generate_menu_view(request):

    prompt = "簡単な夕食"

    result = generate_menu(prompt)

    return JsonResponse(
        {"result": result.model_dump()},
        json_dumps_params={"ensure_ascii": False}
    )

#AIレシピ作成部分
@require_POST
def ai_menu_process(request):

    #未ログイン確認
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "message": "ログインしていません",
                "redirect_url":"/login",
            },
            status=401,
        )
    # JSONの取得
    try:
        request_data =json.loads(request.body)   

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "message": "JSON形式が不正です",
            },
            status=400,
        )
    logger = logging.getLogger(__name__)
    logger.info(request_data)

    # ここでGemini処理
    ai_response =generate_menu(request_data)

    # 一時保存
    Message.objects.create(
        user=request.user,
        content=ai_response.text,
        is_ai=True,
    )

    return JsonResponse(
        {
            "message": "success",
        },
        status=200,
    )


def send_message(request):
    if request.method =='POST':
        
        client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        body = json.loads(request.body)

        request_data = body.get("request_data")

        prompt = f"""
        あなたは優秀な献立メニューアドバイザーです。

        データ:
        {request_data}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return JsonResponse({
            "message": response.text
        })

    return JsonResponse({
        "error": "POST only"
    }, status=400)

#HTMLフォーム
class FoodCreateView(CreateView):
    model = Food
    form_class =FoodForm
    template_name = "foods/food_form.html"
    success_url = reverse_lazy("foods:food-entry")

    
    def form_valid(self, form):
        #追加(NOT NULLであってはならない違反対策)
        form.instance.user = self.request.user

        custom_category = form.cleaned_data.get("custom_category")

        if custom_category:
            category, created = PreFood.objects.get_or_create(
                name=custom_category
            )
            form.instance.category = category

        if form.cleaned_data.get("no_expiration_date"):
            form.instance.expiration_date = None

        return super().form_valid(form)


def register_page(request):
    return render(request, "foods/register.html", using="django")
