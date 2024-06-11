from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15, required=False)
    shipping_address = forms.CharField(max_length=200, required=False)
    birthdate = forms.DateField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'phone_number', 'shipping_address', 'birthdate']
