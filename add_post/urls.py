from django.urls import path

from . import views

app_name = "add_post"

urlpatterns = [
    path("", views.home_page, name="add_post")
]