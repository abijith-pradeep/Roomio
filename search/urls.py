# roomio/search/urls.py

from django.urls import path
from .views import search_home,search_zip,search_interest

from . import views

app_name = "search"

urlpatterns = [
    path("", search_home, name="search_home"),
    path("search_zip/",search_zip,name="search_zip"),
    path("search_interest/",search_interest,name="search_interest")
]