# roomio/search/views.py
from django.db import connection
from django.shortcuts import render

from home.models import Favorite
from .forms import SearchForm, SearchZipRoomForm
from add_post.models import ApartmentUnit, ApartmentBuilding

def search_home(request):
    form = SearchForm(request.POST or None)
    units_data = []

    if request.method == 'POST' and form.is_valid():
        company_name = form.cleaned_data['company_name']
        building_name = form.cleaned_data['building_name']

        # raw_query = """
        # SELECT au.id, au.unit_number, au.monthly_rent, au.square_footage, au.available_date_for_move_in
        # FROM add_post_apartmentunit AS au
        # JOIN add_post_apartmentbuilding AS ab ON au.building_id = ab.id
        
        # """

        raw_query = """
                SELECT au.id, au.unit_number, au.monthly_rent, au.square_footage, au.available_date_for_move_in,
                   ab.id AS building_id, ab.building_name, ab.company_name, ab.address_number, ab.address_street,
                   ab.address_city, ab.address_state, ab.address_zip_code
            FROM add_post_apartmentunit AS au
            INNER JOIN add_post_apartmentbuilding AS ab ON au.building_id = ab.id
            WHERE ab.company_name LIKE %s AND ab.building_name LIKE %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(raw_query, [company_name, building_name])
            units = cursor.fetchall()

            # Get list of unit IDs that are favorited by the user
            cursor.execute("SELECT unit_id FROM home_favorite WHERE user_id = %s", [request.user.id])
            favorites = cursor.fetchall()
            favorite_ids = [item[0] for item in favorites]

        # Create a list of units with favorite status
        
        units_data = [{
            'unit': {
                'id': unit[0],
                'unit_number': unit[1],
                'monthly_rent': unit[2],
                'square_footage': unit[3],
                'available_date_for_move_in': unit[4],
                'building': {
                    'id': unit[5],
                    'building_name': unit[6],
                    'company_name': unit[7],
                    'address_number': unit[8],
                    'address_street': unit[9],
                    'address_city': unit[10],
                    'address_state': unit[11],
                    'address_zip_code': unit[12]
                }
            },
            'is_favourited': unit[0] in favorite_ids
        } for unit in units]

        


        context = {
            "searchForm": form,
            "units_data": units_data
        }
    else:
        context = {
            "searchForm": form,
            "units_data": []
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
        FROM add_post_apartmentunit AS au
        JOIN add_post_apartmentbuilding AS ab ON au.building_id = ab.id
        JOIN (
            SELECT unit_id, 
                SUM(CASE WHEN name LIKE 'bedroom' THEN 1 ELSE 0 END) AS bedroom_count,
                SUM(CASE WHEN name LIKE 'bathroom' THEN 1 ELSE 0 END) AS bathroom_count
            FROM add_post_room
            GROUP BY unit_id
            HAVING SUM(CASE WHEN name LIKE 'bedroom' THEN 1 ELSE 0 END) = %s
            AND SUM(CASE WHEN name LIKE 'bathroom' THEN 1 ELSE 0 END) = %s
            ) AS rooms ON rooms.unit_id = au.id
        WHERE ab.address_zip_code LIKE %s
        GROUP BY ab.address_zip_code;
        """

        with connection.cursor() as cursor:
            cursor.execute(raw_query, [bedrooms, bathrooms, zip_code])
            units = cursor.fetchall()
            print(units)

            # Get list of unit IDs that are favorited by the user
            cursor.execute("SELECT unit_id FROM home_favorite WHERE user_id = %s", [request.user.id])
            favorites = cursor.fetchall()
            favorite_ids = [item[0] for item in favorites]

        # Create a list of units with favorite status
        units_data = [{
            'unit': {
                'average_rent': unit[0],
            },
            'is_favourited': unit[0] in favorite_ids
        } for unit in units]

        context = {
            "searchZipForm": form,
            "units_data": units_data
        }
    else:
        context = {
            "searchZipForm": form,
            "units_data": []  # Ensure units_data is always defined
        }

    return render(request, 'search/search_zip.html', context)
