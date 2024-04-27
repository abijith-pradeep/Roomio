from django.urls import path
from django.urls import path
from .views import register_pet, edit_pet


app_name = "user_profile"

urlpatterns = [
    path('register_pet/', register_pet, name='register_pet'),
    path('edit_pet/<int:pet_id>/', edit_pet, name='edit_pet'),
    # include other URL patterns here
]
