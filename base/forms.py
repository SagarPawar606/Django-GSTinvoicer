from tokenize import Number
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput
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
    name = forms.CharField(max_length=10)
    address = forms.CharField(max_length=10, required=False, widget=forms.Textarea)
    gstin = forms.CharField(max_length=15, required=False, label='GSTIN NO')
    contact_number = forms.CharField(required=False, label='Contact Number')

    #WIDGETS
    name.widget.attrs.update({'class':'form-control', 'placeholder':'Recipient Name'})
    address.widget.attrs.update({'class':'form-control','rows':3, 'placeholder': 'Billing Address'})
    gstin.widget.attrs.update({'class':'form-control','placeholder':'15 digits no.'})
    contact_number.widget.attrs.update({'class':'form-control'})

class InvoiceDetialsForm(forms.Form):
    invoice_no = forms.CharField(max_length=50, label='Invoice Number')
    invoice_date = forms.DateField(label='Invoice Date', widget=forms.TextInput(attrs={'type':'date', 'class':'form-control'}))
    invoice_due = forms.DateField(label='Due Date', required=False, widget=NumberInput(attrs={'type':'date', 'class':'form-control'}))

    #WIDGETS

    invoice_no.widget.attrs.update({'class':'form-control'})
    # invoice_date.widget.attrs.update({'type':'date','class':'form-control'})
    # invoice_due.widget.attrs.update({'type':'date', 'class':'form-control'})

# class ItemDetialsForm(forms.Form):
#     item_name = forms.CharField(max_length=255, label='Item Name')
#     description = forms.CharField(max_length=255, required=False, label='Description')
#     price = forms.
    