from email.policy import default
from tokenize import Number
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import OrganizationlDetials


class UserRegistrationForm(UserCreationForm):
    organization_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'organization_name', 'password1', 'password2']

class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationlDetials
        fields = ['org_name', 'email', 'gstin', 'address', 'contact_no', 'website']


class RecipientDetailsFrom(forms.Form):
    name = forms.CharField(max_length=10,
            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Recipient Name'}))
    address = forms.CharField(max_length=10, required=False, 
            widget=forms.Textarea(attrs={'class':'form-control','rows':3, 'placeholder': 'Billing Address'}))
    gstin = forms.CharField(max_length=15, required=False, label='GSTIN NO',
            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'15 digits no.'}))
    contact_number = forms.CharField(required=False, label='Contact Number',
            widget=forms.TextInput(attrs={'class':'form-control'}))

class InvoiceDetialsForm(forms.Form):
    invoice_no = forms.CharField(max_length=50, label='Invoice Number',
            widget=forms.TextInput(attrs={'class':'form-control'}))
    invoice_date = forms.DateField(label='Invoice Date', 
            widget=forms.TextInput(attrs={'type':'date', 'class':'form-control'}))
    delivery_date = forms.DateField(label='Delivery Date', required=False, 
            widget=forms.TextInput(attrs={'type':'date', 'class':'form-control'}))
    invoice_due = forms.DateField(label='Due Date', required=False, 
            widget=forms.TextInput(attrs={'type':'date', 'class':'form-control'}))
    
class ItemDetialsForm(forms.Form):
    name = forms.CharField(max_length=255, label='Item Name',
            widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=255, required=False, label='Description',
            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Short Description'}))
    hsn_no = forms.CharField(max_length=10, label='HSN/SAC code', required=False,
            widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.DecimalField(decimal_places=2, label='Unit Price',
            widget=forms.NumberInput(attrs={'class':'form-control'}))
    quantity = forms.IntegerField(initial=1 ,label='Quantity', min_value=1,
             widget=forms.NumberInput(attrs={'class':'form-control'}))

class TaxForm(forms.Form):
    discount = forms.DecimalField(decimal_places=2, label='Discount', required=False,
            widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Discount on Total'}))
    cgst = forms.DecimalField(initial=9.0, decimal_places=2, label='CGST %', min_value=0,
            widget=forms.NumberInput(attrs={'class':'form-control'}))
    sgst = forms.DecimalField(initial=9.0, decimal_places=2, label='SGST %', min_value=0,
            widget=forms.NumberInput(attrs={'class':'form-control'}))



    