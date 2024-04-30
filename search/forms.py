from django import forms
from add_post.models import ApartmentBuilding
from django.forms.widgets import NumberInput, DateInput

class SearchForm(forms.Form):
    company_name = forms.CharField(
        label='Company Name', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter company name'})
    )
    building_name = forms.CharField(
        label='Building Name', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter building name'})
    )
    min_rent = forms.IntegerField(
        label='Minimum Rent', 
        required=False, 
        widget=forms.NumberInput(attrs={'min': 0, 'max': 10000, 'step': 50, 'class': 'rent-input'})
    )
    max_rent = forms.IntegerField(
        label='Maximum Rent', 
        required=False, 
        widget=forms.NumberInput(attrs={'min': 0, 'max': 10000, 'step': 50, 'class': 'rent-input'})
    )
    apply_rent_filter = forms.BooleanField(
        label='Apply Rent Filter', 
        required=False, 
        widget=forms.CheckboxInput(attrs={'onclick': 'toggleRentFilters(this.checked)'})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_rent = cleaned_data.get('min_rent')
        max_rent = cleaned_data.get('max_rent')
        apply_rent_filter = cleaned_data.get('apply_rent_filter', False)

        if apply_rent_filter and (min_rent is None or max_rent is None):
            raise forms.ValidationError("Both Minimum Rent and Maximum Rent are required when applying rent filters.")
        if min_rent and max_rent and min_rent > max_rent:
            raise forms.ValidationError("Minimum Rent cannot be greater than Maximum Rent.")
        return cleaned_data


class SearchZipRoomForm(forms.Form):
    zip_code = forms.CharField(max_length=10, required=False, label='Zip Code')
    rooms = forms.IntegerField(initial=1, required=True, label='Number of Bedrooms')
    bathrooms = forms.IntegerField(initial=1,required=True, label='Number of Bathrooms')



class InterestSearchForm(forms.Form):
    roommateCnt = forms.IntegerField(label='Number of Roommates', required=False, widget=NumberInput(attrs={'placeholder': 'Enter number of roommates'}))
    move_in_date = forms.DateField(label='Move-in Date', required=False, widget=DateInput(attrs={'type': 'date'}))
