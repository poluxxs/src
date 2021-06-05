from django import forms
from django.forms import ModelChoiceField

from .models import Product
from .models import Product_tmp
from transactions.models import Transaction

class ProductForm(forms.ModelForm):
    designation = forms.CharField(label = 'Désignation', widget = forms.TextInput(attrs={"placeholder":"Nom du produit"}))
    quantity = forms.IntegerField(label = 'Quantitée',min_value = 1, initial=1)
    price = forms.DecimalField(label = 'Prix',max_digits=6,decimal_places=2,initial=0.00,required=True,min_value=0.00)
    #transaction = forms.ModelChoiceField(widget=forms.Select(),queryset=Transaction.objects.all())
    class Meta:
        model = Product
        fields = [
            'designation',
            'quantity',
            'price',
            #'transaction',
        ]


class ProductForm_tmp(forms.ModelForm):
    designation = forms.CharField(label = 'Désignation', widget = forms.TextInput(attrs={"placeholder":"Nom du produit"}))
    quantity = forms.IntegerField(label = 'Quantitée',min_value = 1, initial=1)
    price = forms.DecimalField(label = 'Prix',max_digits=6,decimal_places=2,initial=0.00,required=True,min_value=0.00)
    class Meta:
        model = Product_tmp
        fields = [
            'designation',
            'quantity',
            'price',
        ]
