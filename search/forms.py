from django import forms
from add_post.models import ApartmentBuilding

class SearchForm(forms.Form):
    company_name = forms.CharField(max_length=100, required=False, label='Company Name')
    building_name = forms.CharField(max_length=100, required=False, label='Building Name')