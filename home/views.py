from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Interest
from django.contrib.auth.decorators import login_required

# Create your views here.

from .models import Interest  # Adjust the import path based on your project structure

def home_page(request):
    interests = Interest.objects.all()  # Fetch all user interests
    return render(request, 'home/home_page.html', {'interests': interests})


@login_required
def like_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if request.user in interest.likes.all():
        interest.likes.remove(request.user)
    else:
        interest.likes.add(request.user)
        interest.dislikes.remove(request.user)  # Ensure user cannot like and dislike simultaneously
    return JsonResponse({'success': True, 'likes': interest.total_likes()})

@login_required
def dislike_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if request.user in interest.dislikes.all():
        interest.dislikes.remove(request.user)
    else:
        interest.dislikes.add(request.user)
        interest.likes.remove(request.user)  # Ensure user cannot like and dislike simultaneously
    return JsonResponse({'success': True, 'dislikes': interest.total_dislikes()})

def logout(request):
    # Clear Django session data
    request.session.clear()
    return redirect("login:index")