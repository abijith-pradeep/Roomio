from django.shortcuts import redirect, render
from django.http import JsonResponse
from .forms import InterestForm
from .models import ApartmentBuilding, ApartmentUnit
# Create your views here.

def home_page(request):
    interestForm = InterestForm()
    

    context = {
            "interestForm": interestForm,
        }
    return render(request, 'add_post/add_post_page.html', context )


def get_buildings(request):
    company_name = request.GET.get('company_name', None)
    if company_name:
        buildings = ApartmentBuilding.objects.filter(company_name=company_name).values_list('building_name', flat=True).distinct()
        print(buildings)
        return JsonResponse(list(buildings), safe=False)
    else:
        return JsonResponse([], safe=False)

def add_interest(request):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            if form.cleaned_data['new_company_name'] and form.cleaned_data['new_building_name']:
                # Create new company and building if not exists
                building, created = ApartmentBuilding.objects.get_or_create(
                    company_name=form.cleaned_data['new_company_name'],
                    building_name=form.cleaned_data['new_building_name'],
                    defaults={'address': form.cleaned_data['address']}
                )
                # Create unit for the new building
                unit = ApartmentUnit.objects.create(
                    unit_number=form.cleaned_data['unit_number'],
                    building=building,
                    # Add other fields as necessary
                )
                interest.unit = unit
            else:
                # If existing company and building are selected
                company_name = form.cleaned_data['company_name']
                building_name = form.cleaned_data['building_name']
                unit_number = form.cleaned_data['unit_number']
                building = ApartmentBuilding.objects.get(company_name=company_name, building_name=building_name)
                unit = ApartmentUnit.objects.create(unit_number=unit_number, building=building)
                interest.unit = unit

            interest.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('home:home')
    else:
        form = InterestForm()
    return render(request, 'add_post_page.html', {'form': form})
