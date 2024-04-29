# roomio/home/views.py

import json
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Favorite, Interest
from .forms import InterestForm
from django.views.decorators.http import require_POST


from add_post.models import ApartmentBuilding, ApartmentUnit, PetPolicy
from user_profile.models import Pet

# Create your views here.

from .models import Interest  # Adjust the import path based on your project structure


def home_page(request):
    if not request.user.is_authenticated:
        return redirect("login:login")
    
    units = ApartmentUnit.objects.all()
    favorites = Favorite.objects.filter(user=request.user).values_list('unit_id', flat=True)
    
    # Include favorite status in the units
    units_data = [{
        'unit': unit,
        'is_favourited': unit.id in favorites
    } for unit in units]

    return render(request, 'home/home_page.html', {'units_data': units_data})


def toggle_favourite(request, unitId):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    try:
        unit = get_object_or_404(ApartmentUnit, id=unitId)
        favorite, created = Favorite.objects.get_or_create(user=request.user, unit=unit)

        if not created:
            # If the favorite exists, we are unfavouriting
            favorite.delete()
            is_favourited = False
        else:
            # Favoriting since the favorite was newly created
            is_favourited = True

        return JsonResponse({'status': 'success', 'is_favourited': is_favourited})
    except ApartmentUnit.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Unit not found'}, status=404)




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

    other_interests = Interest.objects.filter(unit=unit).exclude(user=request.user)

    context = {
        'unit': unit,
        'pet_policies': pet_policies,
        'other_interests': other_interests
    }
    return render(request, 'home/unit_detail.html', context)


def create_interest(request, unit_id):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.user_id = request.user.id
            interest.unit_id = unit_id
            interest.save()
            return redirect('home:home')  # Redirect to the home page after successfully creating the interest
    else:
        form = InterestForm()
    return render(request, 'home/create_interest.html', {'form': form})

def favorite_list(request):
    if not request.user.is_authenticated:
        return redirect('login:login')

    # Using select_related to fetch related unit and building data
    favorites = Favorite.objects.filter(user=request.user).select_related('unit__building')

    # Collecting favorited unit IDs for conditional rendering in the template
    favorite_unit_ids = [fav.unit.id for fav in favorites]

    return render(request, 'home/favorite_page.html', {
        'favorites': favorites,
        'favorite_unit_ids': favorite_unit_ids
    })