from django.urls import path
from .views import search_home

from . import views

app_name = "search"

urlpatterns = [
    path("", search_home, name="search_home"),
]