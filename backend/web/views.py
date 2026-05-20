from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import date
from django.shortcuts import render

def top(request):
    return render(request, "top.html")

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, "home.html", {'today': date.today().strftime('%m月%d日')})

def foodslist(request):
    return render(request, "foodslist.html")

def food_register(request):
    return render(request, "food_register.html")

def pre_foodlist(request):
    return render(request, "pre_foodlist.html")

def favorite_foodslist(request):
    return render(request, "favorite_foodslist.html")

def foodlist_detail(request, food_id):
    return render(request, "foodlist_detail.html", {'food_id': food_id})

# CSRFトークンを送るのに必要なCSRF Cookieを発行する処理
@ensure_csrf_cookie
def signup_view(request):
    return render(request, "signup.html")

@ensure_csrf_cookie
def login_view(request):
    return render(request, "login.html")