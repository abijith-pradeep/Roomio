from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PetForm
from .models import Pet
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib import messages

def userprofile(request):
    if not request.user.is_authenticated:
        return redirect("login:login")
    
    pets = Pet.objects.filter(owner=request.user)
    context = {
        'user': request.user,
        'pets': pets
    }
    return render(request,"user_profile/user_profile.html",context)


def register_pet(request):
    if not request.user.is_authenticated:
        return redirect("login:login")

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PetForm(request.POST)
            if form.is_valid():
                try:
                    pet = form.save(commit=False)
                    pet.owner = request.user  # set the user to the current user
                    pet.save()
                    pets = Pet.objects.filter(owner=request.user)
                    context = {
                        'user': request.user,
                        'pets': pets
                    }
                    return render(request,'user_profile/user_profile.html',context)
                except IntegrityError:
                    messages.error(request, "This pet already exists.")
                except Exception as e:
                    messages.error(request, f"Error registering pet: {str(e)}")
            else:
                messages.error(request, "Please correct the errors below.")
            
    else:
        form = PetForm()
    return render(request, 'user_profile/register_pet.html', {'form': form})


def edit_pet(request, pet_id):
    if not request.user.is_authenticated:
        return redirect("login:login")
    
    pet = Pet.objects.get(id=pet_id, owner=request.user)  # ensure user can only edit their own pets
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            try:
                pets = Pet.objects.filter(owner=request.user).filter(id=pet_id)
                form.save()
                return redirect('user_profile:home')
            except IntegrityError:
                messages.error(request, "This pet already exists.")
            except Exception as e:
                messages.error(request, f"Error registering pet: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PetForm(instance=pet)
    return render(request, 'user_profile/edit_pet.html', {'form': form})
