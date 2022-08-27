from django.forms import ModelForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Item
from django import forms

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'colour', 'size', 'design', 'quantity',)

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'1234 Main St',
        'class': 'form-control w-100'
    }))
    apartment_address = forms.CharField(required = False, widget=forms.TextInput(attrs={
        'placeholder':'Apartment or Suite',
        'class': 'form-control w-100'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control w-100'
    }))
    #same_billing_address = forms.BooleanField(widget = forms.CheckboxInput())
    #save_info = forms.BooleanField(widget = forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget = forms.RadioSelect(), choices=PAYMENT_CHOICES)
