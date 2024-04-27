
from django.shortcuts import render
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

    context = {
        "searchForm": form,
        "units": units
    }
    return render(request, 'search/search_page.html', context)