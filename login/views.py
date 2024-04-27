from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
import django
from .forms import UserSignUpForm
from django.contrib.auth.hashers import make_password
from .signals import user_signed_up, user_logged_in
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse_lazy


# Create your views here.

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
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            hashed_password = make_password(password)
            try:
                User.objects.create(
                    username=username, email=email, password=hashed_password
                )
                data = {"username": username, "email": email}
                user_signed_up(data, request)
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect(
                    "home:home"
                )  # Redirect to login page after successful signup
            except Exception as e:
                print(e)
                return TemplateResponse(
                    request,
                    "login/signup.html",
                    {"form": form, "error": "Error creating user"},
                )
    else:
        form = UserSignUpForm()
    return TemplateResponse(
        request, "login/signup.html", {"form": form, "error": "Error creating user"}
    )


def user_login(request):
    if request.method == "POST":
        form_data = request.POST
        username = form_data.get("username")
        password = form_data.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # user_logged_in(username, request)
            return redirect(
                "home:home"
            )  # Replace 'dashboard' with the desired URL name
        else:
            # If authentication fails, display an error message
            error_message = "Invalid username or password."
            return render(request, "login/login.html", {"error_message": error_message})

    return TemplateResponse(request, "login/login.html")
