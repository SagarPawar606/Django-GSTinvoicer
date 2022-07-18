from email.policy import default
from tokenize import Number
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import OrganizationlDetials
from datetime import date
from django.forms import formset_factory

class UserRegistrationForm(UserCreationForm):
    organization_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'organization_name', 'password1', 'password2']

class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationlDetials
        fields = ['org_name', 'email', 'gstin', 'address', 'contact_no', 'website']


class RecipientDetailsForm(forms.Form):
    rcpt_name = forms.CharField(max_length=10, label='Recipient Name',
            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Recipient Name'}))
    b_address = forms.CharField(max_length=255, required=False, label='Billing Address',
            widget=forms.Textarea(attrs={'class':'form-control','rows':3, 'placeholder': 'Billing Address'}))
    addr_chk_box = forms.BooleanField(required=False, label='Both addresses are same')
    s_address = forms.CharField(max_length=255, required=False, label='Shipping Address',
            widget=forms.Textarea(attrs={'class':'form-control','rows':3, 'placeholder': 'Shipping Address'}))
    gstin = forms.CharField(max_length=15, required=False, label='GSTIN NO',
            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'15 digit no.'}))
    contact_number = forms.CharField(required=False, label='Contact Number',
            widget=forms.TextInput(attrs={'class':'form-control'}))

class InvoiceDetialsForm(forms.Form):
    invoice_no = forms.CharField(max_length=50, label='Invoice Number',
            widget=forms.TextInput(attrs={'class':'form-control'}))
    invoice_date = forms.DateField(initial=date.today(), label='Invoice Date', 
            widget=forms.TextInput(attrs={'type':'date', 'class':'form-control'}))
    delivery_date = forms.DateField(label='Delivery Date', required=False, 
            widget=forms.TextInput(attrs={'type':'date', 'class':'form-control'}))
    due_date = forms.DateField(label='Due Date', required=False, 
            widget=forms.TextInput(attrs={'type':'date', 'class':'form-control'}))
    
class ItemDetialsForm(forms.Form):
    item_name = forms.CharField(max_length=255, label='Item Name',
            widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
    description = forms.CharField(max_length=255, required=False, label='Description',
            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Short Description'}))
    hsn_no = forms.CharField(max_length=10, label='HSN/SAC code', required=False,
            widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.DecimalField(decimal_places=2, label='Unit Price',
            widget=forms.NumberInput(attrs={'class':'form-control','required':'required'}))
    quantity = forms.IntegerField(initial=1 ,label='Quantity', min_value=1,
             widget=forms.NumberInput(attrs={'class':'form-control','required':'required'}))
    cgst = forms.DecimalField(initial=9.0, decimal_places=2, label='CGST %', min_value=0,
             widget=forms.NumberInput(attrs={'class':'form-control','required':'required'}))
    sgst = forms.DecimalField(initial=9.0, decimal_places=2, label='SGST %', min_value=0,
            widget=forms.NumberInput(attrs={'class':'form-control','required':'required'}))

class ExtraChargesForm(forms.Form):
    discount = forms.DecimalField(initial=0, min_value=0, decimal_places=2, label='Discount', required=False,
            widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Discount on Total'}))
    shipping = forms.DecimalField(initial=0, min_value=0, decimal_places=2, label='Shipping Charges', required=False,
            widget=forms.NumberInput(attrs={'class':'form-control'}))
    

ItemsFormset = formset_factory(ItemDetialsForm, extra=1)

    