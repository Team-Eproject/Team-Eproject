from datetime import date

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from apps.foods.forms import FoodForm
from apps.foods.models import Food, PreFood, FoodTemplate
from apps.shopping_memos.models import ShoppingMemo
from django.views.decorators.http import require_POST

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

    # 今日が期限の食品(アラート用)
    today_expiry_foods = (
        Food.objects
        .select_related("category")
        .filter(
            user=request.user,
            no_expiration_date=False,
            expiration_date=today,
        )
        .order_by("created_at")
    )

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

    # 期限切れの食品があるときのみまとめて削除ボタン表示
    expired_food_count = Food.objects.filter(
    user=request.user,
    no_expiration_date=False,
    expiration_date__lt=today,
    ).count()

    return render(request, "home.html", {
        "today": today.strftime("%m月%d日"),
        "user": request.user,
        "today_expiry_foods": build_food_cards(today_expiry_foods, today),
        "near_expiry_foods": build_food_cards(near_expiry_foods, today),
        "recent_foods": build_food_cards(recent_foods, today),
        "registered": request.GET.get("registered") == "1",
        "deleted_expired": request.GET.get("deleted_expired") == "1",
        "expired_food_count": expired_food_count,
    })

@login_required
def foodslist(request):
    today = date.today()

    sort = request.GET.get("sort", "expiry_asc")
    category_id = request.GET.get("category", "")

    foods = (
        Food.objects
        .select_related("category")
        .filter(user=request.user)
    )

    if category_id:
        foods = foods.filter(category_id=category_id)

    if sort == "created_desc":
        foods = foods.order_by("-created_at")
    elif sort == "created_asc":
        foods = foods.order_by("created_at")
    elif sort == "expiry_desc":
        foods = foods.order_by("-expiration_date")
    else:
        foods = foods.order_by("expiration_date", "-created_at")

    categories = PreFood.objects.all()

    return render(request, "foodslist.html", {
        "foods": build_food_cards(foods, today),
        "categories": categories,
        "selected_sort": sort,
        "selected_category_id": category_id,
    })

@login_required
def food_register(request):
    categories = PreFood.objects.all()

    template_id = request.GET.get("template_id")
    selected_template = None

    if template_id:
        selected_template = get_object_or_404(
            FoodTemplate.objects.select_related("category"),
            id=template_id,
        )

    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)

        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user

            # 食品プリセットから選んだ場合、画像未アップロードならデフォルト画像をコピー
            template_id = request.POST.get("template_id")
            if template_id and not food.image:
                template = get_object_or_404(FoodTemplate, id=template_id)
                food.image = template.image

            food.save()
            return redirect("/home/?registered=1")

    else:
        initial = {}

        if selected_template:
            initial = {
                "name": selected_template.name,
                "category": selected_template.category,
            }

        form = FoodForm(initial=initial)

    return render(request, "food_register.html", {
        "form": form,
        "categories": categories,
        "selected_template": selected_template,
    })

@login_required
def pre_foodlist(request):
    categories = PreFood.objects.all()

    q = request.GET.get("q", "")
    category_id = request.GET.get("category", "")

    prefoods = FoodTemplate.objects.select_related("category").all()

    if q:
        prefoods = prefoods.filter(name__icontains=q)

    if category_id:
        prefoods = prefoods.filter(category_id=category_id)

    return render(request, "pre_foodlist.html", {
        "prefoods": prefoods,
        "categories": categories,
        "q": q,
        "selected_category_id": category_id,
    })

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
    
@login_required
@require_POST
def delete_expired_foods(request):
    today = date.today()

    Food.objects.filter(
        user=request.user,
        no_expiration_date=False,
        expiration_date__lt=today,
    ).delete()

    return redirect("/home/?deleted_expired=1")

@login_required
@require_POST
def delete_food(request, food_id):
    food = get_object_or_404(
        Food,
        id=food_id,
        user=request.user,
    )

    food.delete()

    next_url = request.POST.get("next") or "foodslist"

    if next_url == "home" or "foodlist_detail":
        return redirect("home")

    return redirect("foodslist")

@login_required
def user_info(request):
    food_count = Food.objects.filter(user=request.user).count()

    return render(request, "user_info.html", {
        "user": request.user,
        "food_count": food_count,
    })

@login_required
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("top")

    return redirect("user_info")

# メモリスト
@login_required
def memolist(request):
    memos = ShoppingMemo.objects.filter(user=request.user)

    return render(request, "memolist.html", {
        "memos": memos,
    })

# メモ新規作成
@login_required
def memo_register(request):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            ShoppingMemo.objects.create(
                user=request.user,
                content=content,
            )

        return redirect("memolist")

    return render(request, "memo_register.html")

# メモ詳細
@login_required
def memo_detail(request, memo_id):
    memo = get_object_or_404(
        ShoppingMemo,
        id=memo_id,
        user=request.user,
    )

    return render(request, "memo_detail.html", {
        "memo": memo,
    })

# メモ削除
@login_required
def memo_delete(request, memo_id):
    memo = get_object_or_404(
        ShoppingMemo,
        id=memo_id,
        user=request.user,
    )

    if request.method == "POST":
        memo.delete()

    return redirect("memolist")

# メモ更新
@login_required
def memo_edit(request, memo_id):
    memo = get_object_or_404(
        ShoppingMemo,
        id=memo_id,
        user=request.user,
    )

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            memo.content = content
            memo.save()

        return redirect("memo_detail", memo_id=memo.id)

    return render(request, "memo_register.html", {
        "memo": memo,
        "is_edit": True,
    })

# AIレシピ機能
@login_required
def recipe(request):
    foods = (
        Food.objects
        .select_related("category")
        .filter(user=request.user)
        .order_by("expiration_date", "-created_at")
    )

    selected_foods = []
    recipe_result = None
    error_message = None

    if request.method == "POST":
        selected_ids = request.POST.getlist("food_ids")

        if not selected_ids:
            error_message = "食材を1つ以上選んでください。"
        else:
            selected_foods = list(
                Food.objects
                .filter(
                    id__in=selected_ids,
                    user=request.user,
                )
                .select_related("category")
            )

            food_names = [food.name for food in selected_foods]

            # ここを後でAI API呼び出しに差し替える
            recipe_result = generate_recipe_text(food_names)

    return render(request, "recipe.html", {
        "foods": foods,
        "selected_foods": selected_foods,
        "recipe_result": recipe_result,
        "error_message": error_message,
    })


def generate_recipe_text(food_names):
    """
    1日実装用の仮レシピ生成。
    後でバックエンド担当のAI処理に差し替える。
    """
    ingredients = "、".join(food_names)

    return f"""
おすすめレシピ：{ingredients}の簡単炒め

【使う食材】
{ingredients}

【作り方】
1. 食材を食べやすい大きさに切ります。
2. フライパンで火の通りにくい食材から炒めます。
3. 塩こしょう、しょうゆ、またはめんつゆで味付けします。
4. 全体に火が通ったら完成です。

【ポイント】
賞味期限が近い食材から使うと、冷蔵庫の整理にもなります。
"""


# CSRFトークンを送るのに必要なCSRF Cookieを発行する処理
@ensure_csrf_cookie
def signup_view(request):
    return render(request, "signup.html")

@ensure_csrf_cookie
def login_view(request):
    return render(request, "login.html")
