from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Interest
from django.contrib.auth.decorators import login_required

from add_post.models import ApartmentBuilding, ApartmentUnit, PetPolicy
from user_profile.models import Pet

# Create your views here.

from .models import Interest  # Adjust the import path based on your project structure


def home_page(request):
    if request.user.is_authenticated:
        interests = Interest.objects.all()  # Fetch all user interests
        return render(request, 'home/home_page.html', {'interests': interests})

    else:
        return redirect("login:login")


def like_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if request.user in interest.likes.all():
        interest.likes.remove(request.user)
    else:
        interest.likes.add(request.user)
        interest.dislikes.remove(request.user)  # Ensure user cannot like and dislike simultaneously
    return JsonResponse({'success': True, 'likes': interest.total_likes()})


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
    return redirect("login:login")

def unit_details(request, unit_id):
    unit = get_object_or_404(ApartmentUnit, pk=unit_id)
    user_pets = Pet.objects.filter(owner=request.user)
    pet_policies = []

    for user_pet in user_pets:
        pet_policy = PetPolicy.objects.filter(
            apartment_building=unit.building,
            pet_type=user_pet.pet_type,
            pet_size=user_pet.pet_size
        ).first()

        if pet_policy:
            pet_policies.append({
                'pet_type': user_pet.pet_type,
                'pet_size': user_pet.pet_size,
                'allowed': pet_policy.is_allowed,
                'registration_fee': pet_policy.registration_fee,
                'monthly_fee': pet_policy.monthly_fee
            })

    context = {
        'unit': unit,
        'pet_policies': pet_policies
    }
    return render(request, 'home/unit_detail.html', context)