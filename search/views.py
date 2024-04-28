
from django.shortcuts import render

from home.models import Favorite
from .forms import SearchForm
from add_post.models import ApartmentUnit, ApartmentBuilding

def search_home(request):
    form = SearchForm(request.POST or None)
    units = []

    if request.method == 'POST' and form.is_valid():
        company_name = form.cleaned_data['company_name']
        building_name = form.cleaned_data['building_name']

        # Filter apartment units based on building and company name
        units = ApartmentUnit.objects.filter(
            building__company_name=company_name,
            building__building_name=building_name
        )

        # Get list of unit IDs that are favorited by the user
        favorites = Favorite.objects.filter(user=request.user).values_list('unit_id', flat=True)

        # Create a list of units with favorite status
        units_data = [{
            'unit': unit,
            'is_favourited': unit.id in favorites
        } for unit in units]

        context = {
            "searchForm": form,
            "units_data": units_data  # Pass units data with favorite status
        }
    else:
        context = {
            "searchForm": form,
            "units_data": []  # Ensure units_data is always defined
        }

    return render(request, 'search/search_page.html', context)