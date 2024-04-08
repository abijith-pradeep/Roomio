from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from .models import Interest  # Adjust the import path based on your project structure

def home_page(request):
    interests = Interest.objects.all()  # Fetch all user interests
    return render(request, 'home/home_page.html', {'interests': interests})