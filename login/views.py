from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse

from django.http import HttpResponse
from django.db import connection
from django.template.response import TemplateResponse
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


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
        return render("home:home")
    return render(request, "login/signup.html")

def user_signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            hashed_password = make_password(form.cleaned_data['password'])
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO login_user (username, first_name, last_name, email, password, dob, gender, is_active, is_staff, is_superuser, date_joined, phone)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)
                """, [
                    form.cleaned_data['username'],
                    form.cleaned_data['first_name'],
                    form.cleaned_data['last_name'],
                    form.cleaned_data['email'],
                    hashed_password,
                    form.cleaned_data['dob'],
                    form.cleaned_data['gender'],
                    "True",
                    "False",
                    "False",
                    timezone.now(),
                    form.cleaned_data['phone']
,                ])
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
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
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM login_user WHERE username = %s", [username])
            row = cursor.fetchone()
            if row is not None:
                hashed_password = row[0]
                if check_password(password, hashed_password):  # Check the hashed password
                    user = User.objects.get(username=username)
                    login(request, user)
                    request.session['test'] = 'This is a test.'
                    # Redirect to the home page
                    return redirect("home:home")
    return TemplateResponse(request, "login/login.html", {"error_message": "Invalid username or password."})


