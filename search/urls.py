from django.urls import path
from .views import search_home,search_zip

from . import views

app_name = "search"

urlpatterns = [
    path("", search_home, name="search_home"),
    path("search_zip/",search_zip,name="search_zip")
]