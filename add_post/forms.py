# forms.py
from django import forms
from .models import ApartmentBuilding, Amenities, ApartmentUnit, PetPolicy
from home.models import Interest

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['unit', 'move_in_date', 'roommate_count']

    company_name = forms.ChoiceField(
        choices=[('', 'Select Company'), ('Other', 'Other')] + 
                list(ApartmentBuilding.objects.all().values_list('company_name', 'company_name').distinct()),
        required=True,
        label='Company Name'
    )
    building_name = forms.ChoiceField(
        choices=[('', 'Select Building')],
        required=False,
        label='Building Name'
    )

    new_company_name = forms.CharField(max_length=100, required=False, label='New Company Name')
    new_building_name = forms.CharField(max_length=100, required=False, label='New Building Name')

    unit_number = forms.CharField(max_length=50, label='Unit Number')
    address = forms.CharField(max_length=255, label='Address')
    pet_policy = forms.ModelChoiceField(
        queryset=PetPolicy.objects.all(),
        required=False,
        label='Pet Policy'
    )
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super(InterestForm, self).__init__(*args, **kwargs)
        # Set initial queryset for building_name field
        self.fields['building_name'].choices = self.get_building_choices()
        
    def get_building_choices(self):
        # Provide initial choices for building_name field
        return [('', 'Select Building')]

    def clean(self):
        cleaned_data = super().clean()
        company_name = cleaned_data.get("company_name")
        new_company_name = cleaned_data.get("new_company_name")
        if company_name == 'Other' and not new_company_name:
            self.add_error('new_company_name', 'This field is required if "Other" is selected.')
        return cleaned_data
