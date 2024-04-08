from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.login_redirect, name="login"),
    path("signup/", views.signup, name="signup"),
    path("userSignup/", views.user_signup, name="userSignup"),
    path("userLogin/", views.user_login, name="userLogin"),
]