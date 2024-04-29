from django import forms
from add_post.models import ApartmentBuilding

class SearchForm(forms.Form):
    company_name = forms.CharField(max_length=100, required=False, label='Company Name')
    building_name = forms.CharField(max_length=100, required=False, label='Building Name')

class SearchZipRoomForm(forms.Form):
    zip_code = forms.CharField(max_length=10, required=False, label='Zip Code')
    rooms = forms.IntegerField(initial=1, required=True, label='Number of Bedrooms')
    bathrooms = forms.IntegerField(initial=1,required=True, label='Number of Bedrooms')