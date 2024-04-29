
from django.shortcuts import render

from home.models import Favorite
from .forms import SearchForm, SearchZipRoomForm
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

def search_zip(request):
    form = SearchZipRoomForm(request.POST or None)
    units_data = []

    if request.method == 'POST' and form.is_valid():
        zip_code = form.cleaned_data.get('zip_code', '')
        bedrooms = form.cleaned_data.get('rooms', 1)
        bathrooms = form.cleaned_data.get('bathrooms',1)

        raw_query = f"""
        SELECT AVG(au.monthly_rent) AS average_rent
        FROM apartment_unit AS au
        JOIN apartment_building AS ab ON au.building_id = ab.id
        JOIN (
            SELECT unit_id, 
                SUM(CASE WHEN name = 'bedroom' THEN 1 ELSE 0 END) AS bedroom_count,
                SUM(CASE WHEN name = 'bathroom' THEN 1 ELSE 0 END) AS bathroom_count
            FROM room
            GROUP BY unit_id
            HAVING SUM(CASE WHEN name = 'bedroom' THEN 1 ELSE 0 END) = %s
            AND SUM(CASE WHEN name = 'bathroom' THEN 1 ELSE 0 END) = %s
            ) AS rooms ON rooms.unit_id = au.id
        WHERE ab.address_zip_code LIKE %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(raw_query, [bedroom + '%', bathroom + '%', zip_code + '%', rooms])
            result = cursor.fetchall()

        # Create a list of units with favorite status
        favorites = Favorite.objects.filter(user=request.user).values_list('unit_id', flat=True)

        # Create a list of units with favorite status
        units_data = [{
            'unit': unit,
            'is_favourited': unit.id in favorites
        } for unit in units]

        context = {
            "searchZipForm": form,
            "units_data": units_data  # Pass units data with favorite status
        }
    else:
        context = {
            "searchZipForm": form,
            "units_data": []  # Ensure units_data is always defined
        }

    return render(request, 'search/search_zip.html', context)
