# roomio/home/urls.py

from django.urls import path
from . import views
from .views import toggle_favourite

app_name = "home"

urlpatterns = [
    path("", views.home_page, name="home"),  
    path("logout/", views.logout, name="logout"), 
    path('unit/<str:unit_id>/', views.unit_details, name='view_detail'), 
    path("unit/<str:unit_id>/create_interest/", views.create_interest, name="create_interest"),
    path('favorite/toggle_favorite/<int:unitId>/', views.toggle_favourite, name='toggle_favorite'),
    path("favorite/", views.favorite_list, name="favorite_page")
]