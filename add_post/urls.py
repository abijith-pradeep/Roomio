from django.urls import path

from . import views

app_name = "add_post"

urlpatterns = [
    path('', views.home_page, name='add_post'),
    path('add_interest/', views.add_interest, name='add_interest'),
    path('get_buildings/', views.get_buildings, name='get_buildings'),
]