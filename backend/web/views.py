from django.shortcuts import render
from apps.foods.forms import FoodForm

def top(request):
    return render(request, "top.html")

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def main(request):
    return render(request, "main.html")

#def foods(request):

    form = FoodForm()

    return render(
        request,
        "foods/food_form.html",
        {"form": form}
    )