from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.template.response import TemplateResponse

from .models import User
from .forms import UserSignUpForm

def index(request):
    return HttpResponse("Hello User")

def login_redirect(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    return render(request, "login/login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def signup(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    return render(request, "login/signup.html")

def user_signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Use form.save() if you implement the model form
            login(request, user)
            return redirect("home:home")
        else:
            return render(request, "login/signup.html", {"form": form})
    else:
        form = UserSignUpForm()
    return render(request, "login/signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home:home")
        else:
            return render(request, "login/login.html", {"error_message": "Invalid username or password."})
    return TemplateResponse(request, "login/login.html")
