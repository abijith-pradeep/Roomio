from django.urls import path
from . import views
from .views import toggle_favourite

app_name = "home"

urlpatterns = [
    path("", views.home_page, name="home"),  
    path("logout/", views.logout, name="logout"), 
    path('unit/<str:unit_id>/', views.unit_details, name='view_detail'),
    path("interests/<int:interest_id>/like/", views.toggle_favourite, name='toggle_favourite'),  
    path("unit/<str:unit_id>/create_interest/", views.create_interest, name="create_interest"),
]