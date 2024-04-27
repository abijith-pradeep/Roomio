from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PetForm
from .models import Pet
from django.http import HttpResponse

@login_required
def register_pet(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PetForm(request.POST)
            if form.is_valid():
                pet = form.save(commit=False)
                pet.user = request.user  # set the user to the current user
                pet.save()
                return redirect('profile')  # redirect to the profile page or wherever appropriate
    else:
        form = PetForm()
    return render(request, 'register_pet.html', {'form': form})

@login_required
def edit_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id, user=request.user)  # ensure user can only edit their own pets
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PetForm(instance=pet)
    return render(request, 'edit_pet.html', {'form': form})
