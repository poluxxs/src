from django import forms

from django.forms import ModelChoiceField

from .models import Transaction
from clients.models import Client
from products.models import Product

from django import forms

class DateInput(forms.DateInput):
    input_type = 'datetime'

class TransactionForm(forms.ModelForm):
    client = forms.ModelChoiceField(widget=forms.Select(),label = '',queryset=Client.objects.all())
    description = forms.CharField(required=False,label = 'Description', widget = forms.Textarea(attrs={"placeholder":"Description ou détail supplémentaire"}))
    delivery_fee = forms.DecimalField(label = 'Frais de livraison',max_digits=6,decimal_places=2,initial=0.00,required=True,min_value=0.00,help_text='A valid email address, please.')
    delivery_location_1 = forms.CharField(label = 'Adresse de livraison', widget = forms.TextInput(attrs={"placeholder":"Rue"}))
    delivery_location_2 = forms.CharField(label = '', widget = forms.TextInput(attrs={"placeholder":"Localitée"}))
    delivery_date = forms.DateField(label = 'Date',widget=forms.DateInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control',
               'placeholder': 'Select a date',
               'type': 'date'
              }))#attrs={'class': 'datepicker', 'type': 'date'}))
    delivery_time = forms.TimeField(label = 'Heure',widget=forms.TimeInput(attrs={'class': 'datepicker',  'type': 'time'}))

        #forms.DateField(required=False, label = 'Date & heure')
    class Meta:
        model = Transaction
        fields = [
            'client',
            'description',
            'delivery_fee',
            'delivery_location_1',
            'delivery_location_2',
            'delivery_date',
            'delivery_time',
        ]

        #widgets = {
                    #'delivery_date': DateInput(),
                #}
 #widget=DateTimePickerInput(attrs={"placeholder":"Date de livraison"})
