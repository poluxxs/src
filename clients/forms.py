from django import forms

from django.forms import ModelChoiceField
from django.db import IntegrityError

from .models import Client

TITLE_CHOICES = [
    ('Monsieur', 'Monsieur'),
    ('Madame', 'Madame'),
]

class ClientForm(forms.ModelForm):
    designation = forms.CharField(
        max_length=10,
        widget=forms.Select(choices=TITLE_CHOICES),
    )
    name = forms.CharField(label = 'Nom', widget = forms.TextInput(attrs={"placeholder":"Nom"}))
    firstName = forms.CharField(label = 'Prénom', widget = forms.TextInput(attrs={"placeholder":"Prénom"}))#,error_messages={'required': 'gwrg enter your name'})
    street = forms.CharField(label = 'Rue', widget = forms.TextInput(attrs={"placeholder":"Rue"}))
    city = forms.CharField(label = 'Ville', initial='St-Aubin', widget = forms.TextInput(attrs={"placeholder":"Ville"}))
    postal_code = forms.IntegerField(label = 'CP', min_value = 1000, max_value=9999, initial=1566)
    email = forms.EmailField(label = 'E-Mail',required=False)
    class Meta:
        model = Client
        fields = [
            'designation',
            'name',
            'firstName',
            'street',
            'city',
            'postal_code',
            'email',
        ]
