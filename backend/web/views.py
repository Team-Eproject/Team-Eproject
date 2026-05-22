from django.shortcuts import render
from apps.foods.forms import FoodForm
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import date
from django.shortcuts import render
from apps.foods.models import Food
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

def top(request):
    return render(request, "top.html")

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def build_food_cards(foods, today):
    """
    Foodモデルのデータを、テンプレートで表示しやすい形に変換する関数
    """
    food_cards = []

    for food in foods:
        # 賞味期限なし、または賞味期限が未入力の場合
        if food.no_expiration_date or food.expiration_date is None:
            days_left = None
            expiration_display = "期限なし"
        else:
            days_left = (food.expiration_date - today).days
            expiration_display = food.expiration_date.strftime("%m月%d日")

        food_cards.append({
            "id": food.id,
            "name": food.name,
            "category_name": food.custom_category or food.category.name,
            "quantity": food.quantity,
            "days_left": days_left,
            "expiration_display": expiration_display,
            "image_url": food.image.url if food.image else None,
            "created_at_display": food.created_at.strftime("%Y年%m月%d日"),
        })

    return food_cards

@login_required
def home(request):
    today = date.today()

    # 期限が近い食品
    # 賞味期限なし・賞味期限未入力の食品は除外
    near_expiry_foods = (
        Food.objects
        .select_related("category")
        .filter(
            # ログイン中のユーザーが登録した食品だけ表示
            user=request.user,
            no_expiration_date=False,
            expiration_date__isnull=False,
        )
        .order_by("expiration_date")[:3]
    )

    # 最近登録した食品
    # 期限なし食品も含める
    recent_foods = (
        Food.objects
        .select_related("category")
        # ログイン中のユーザーが登録した食品だけ表示
        .filter(user=request.user)
        .order_by("-created_at")[:3]
    )

    return render(request, "home.html", {
        "today": today.strftime("%m月%d日"),
        "user": request.user,
        "near_expiry_foods": build_food_cards(near_expiry_foods, today),
        "recent_foods": build_food_cards(recent_foods, today),
    })

@login_required
def foodslist(request):
    today = date.today()

    foods = (
        Food.objects
        .select_related("category")
        .filter(user=request.user)
        .order_by("expiration_date", "-created_at")
    )

    return render(request, "foodslist.html", {
        "foods": build_food_cards(foods, today),
    })

def food_register(request):
    return render(request, "food_register.html")

def pre_foodlist(request):
    return render(request, "pre_foodlist.html")

def favorite_foodslist(request):
    return render(request, "favorite_foodslist.html")

@login_required
def foodlist_detail(request, food_id):
    food = get_object_or_404(
        Food.objects.select_related("category"),
        id=food_id,
        user=request.user,
    )

    today = date.today()

    if food.no_expiration_date or food.expiration_date is None:
        days_left = None
        expiration_display = "期限なし"
        expiration_detail_display = "期限なし"
    else:
        days_left = (food.expiration_date - today).days
        expiration_display = food.expiration_date.strftime("%m月%d日")
        expiration_detail_display = food.expiration_date.strftime("%Y年%m月%d日")

    food_detail = {
        "id": food.id,
        "name": food.name,
        "category_name": food.custom_category or food.category.name,
        "quantity": food.quantity,
        "days_left": days_left,
        "expiration_display": expiration_display,
        "expiration_detail_display": expiration_detail_display,
        "created_at_display": food.created_at.strftime("%Y年%m月%d日"),
        "image_url": food.image.url if food.image else None,
    }

    return render(request, "foodlist_detail.html", {
        "food": food_detail,
    })

def foods(request):
    form = FoodForm()
    
    return render(
        request,
        "foods/food_form.html",
        {"form": form}
    )
    

    
# CSRFトークンを送るのに必要なCSRF Cookieを発行する処理
@ensure_csrf_cookie
def signup_view(request):
    return render(request, "signup.html")

@ensure_csrf_cookie
def login_view(request):
    return render(request, "login.html")
