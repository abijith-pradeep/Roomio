from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()

GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Other'),
)

class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # Ensure the password field uses a password input widget

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'gender', 'dob', 'phone']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hashes the password properly
        if commit:
            user.save()
        return user
