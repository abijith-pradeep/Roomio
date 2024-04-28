from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Interest
from .forms import InterestForm



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


def like_interest(request):
    interest_id = request.POST.get('interest_id')
    try:
        interest = Interest.objects.get(id=interest_id)
        interest.like()  # Calls the like method to increment the like count
        return JsonResponse({'status': 'success', 'total_likes': interest.total_likes})
    except Interest.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Interest not found'}, status=404)

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