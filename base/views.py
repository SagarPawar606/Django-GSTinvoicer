from django.shortcuts import redirect, render
from .forms import (UserRegistrationForm, 
                    OrganizationProfileForm, 
                    RecipientDetailsForm,
                    InvoiceDetialsForm,
                    ExtraChargesForm,
                    ItemsFormset)
from .models import OrganizationlDetials
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            organization_name = form.cleaned_data.get('organization_name')
            print(f'Registration Successfull for {username}')

            user = User.objects.get(username=username)
            org_obj = OrganizationlDetials.objects.create(user=user, org_name=organization_name)
            org_obj.save()
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'base/registration.html', {'form':form})

def index(request):
    return render(request, 'base/index.html')

@login_required
def orgnization_profile(request):
    if request.method == 'POST':
        form = OrganizationProfileForm(request.POST, instance=request.user.organizationldetials)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OrganizationProfileForm(instance=request.user.organizationldetials)
    
    return render(request, 'base/profile.html', {'form':form})

@login_required
def invoice(request):
    if request.method == 'POST':
        rcpt_form = RecipientDetailsForm(request.POST)
        inv_detail_form = InvoiceDetialsForm(request.POST)
        item_formset = ItemsFormset(request.POST)
        extra_form = ExtraChargesForm(request.POST)
        if rcpt_form.is_valid() and inv_detail_form.is_valid() and item_formset.is_valid() and extra_form.is_valid():
            name = rcpt_form.cleaned_data['rcpt_name']
            print(name)
    else:
        rcpt_form = RecipientDetailsForm()
        inv_detail_form = InvoiceDetialsForm()
        item_formset = ItemsFormset()
        extra_form = ExtraChargesForm()
        
    context = {'rcpt_form' : rcpt_form, 
                'inv_det_form' : inv_detail_form, 
                'item_formset':item_formset,
                'extra_form': extra_form,    
                }
    
    return render(request, 'base/invoice.html', context)


