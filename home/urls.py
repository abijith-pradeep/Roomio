from django.urls import path
from . import views
from .views import like_interest, dislike_interest

app_name = "home"

urlpatterns = [
    path("", views.home_page, name="home"),  
    path("logout/", views.logout, name="logout"),  
    path("interests/<int:interest_id>/like/", views.like_interest, name='like_interest'),  
    path("interests/<int:interest_id>/dislike/", views.dislike_interest, name='dislike_interest'),  
]