from django import forms
from .models import Interest

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['move_in_date', 'roommate_count']

    def __init__(self, *args, **kwargs):
        super(InterestForm, self).__init__(*args, **kwargs)
        self.fields['move_in_date'].widget = forms.DateInput(attrs={'type': 'date'})
