from django.shortcuts import render
from apps.foods.forms import FoodForm
from django.views.decorators.csrf import ensure_csrf_cookie

def top(request):
    return render(request, "top.html")

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def main(request):
    return render(request, "main.html")

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
