from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PetForm
from .models import Pet
from django.http import HttpResponse
from django.db import IntegrityError, connection
from django.contrib import messages

def userprofile(request):
    if not request.user.is_authenticated:
        return redirect("login:login")
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_profile_pet WHERE owner_id = %s", [request.user.id])
        pets = cursor.fetchall()

    context = {
        'user': request.user,
        'pets': [dict(zip([column[0] for column in cursor.description], pet)) for pet in pets]
    }
    return render(request,"user_profile/user_profile.html",context)


def register_pet(request):
    if not request.user.is_authenticated:
        return redirect("login:login")

    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO user_profile_pet (pet_name, pet_type, pet_size, owner_id) VALUES (%s, %s, %s, %s)",
                                   [form.cleaned_data['pet_name'], form.cleaned_data['pet_type'], form.cleaned_data['pet_size'], request.user.id])
                    return redirect('user_profile:home')
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
    
    pet = None  # Initialize pet variable for later use
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE user_profile_pet SET pet_name = %s, pet_type = %s, pet_size = %s WHERE id = %s AND owner_id = %s",
                                   [form.cleaned_data['pet_name'], form.cleaned_data['pet_type'], form.cleaned_data['pet_size'], pet_id, request.user.id])
                return redirect('user_profile:home')
            except IntegrityError:
                messages.error(request, "This pet already exists.")
            except Exception as e:
                messages.error(request, f"Error updating pet: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_profile_pet WHERE id = %s AND owner_id = %s", [pet_id, request.user.id])
            pet = cursor.fetchone()
            form = PetForm(initial=dict(zip([column[0] for column in cursor.description], pet)))
    return render(request, 'user_profile/edit_pet.html', {'form': form})
