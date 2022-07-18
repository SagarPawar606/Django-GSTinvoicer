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
from pprint import pprint
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

        invoice_dict = {}
        if rcpt_form.is_valid() and inv_detail_form.is_valid() and extra_form.is_valid() and item_formset.is_valid():
            # recipient details
            invoice_dict['rcpt_name'] = str(rcpt_form.cleaned_data['rcpt_name'])
            invoice_dict['gstin'] = str(rcpt_form.cleaned_data['gstin'])
            invoice_dict['contact_number'] = str(rcpt_form.cleaned_data['contact_number'])
            invoice_dict['b_address'] = str(rcpt_form.cleaned_data['b_address'])
            invoice_dict['s_address'] = str(rcpt_form.cleaned_data['s_address'])
            # invoice detials
            invoice_dict['invoice_no'] = str(inv_detail_form.cleaned_data['invoice_no'])
            invoice_dict['invoice_date'] = str(inv_detail_form.cleaned_data['invoice_date'])
            invoice_dict['delivery_date'] = str(inv_detail_form.cleaned_data['delivery_date'])
            invoice_dict['due_date'] = str(inv_detail_form.cleaned_data['due_date'])
            
        pprint(invoice_dict)
        print()
        
        if item_formset.is_valid() and extra_form.is_valid():
            items_dict = {}
            before_tax_total = 0
            after_tax_total = 0
            
            def calculate_gst(price, quantity, cgst, sgst):
                price = price * quantity
                cgst_value = (price/100) * cgst
                sgst_value = (price/100) * sgst
                return price + cgst_value + sgst_value

            for i, form in enumerate(item_formset, start=1):
                if form.is_valid():
                    price = form.cleaned_data['price']
                    quantity = form.cleaned_data['quantity']
                    cgst = form.cleaned_data['cgst']
                    sgst = form.cleaned_data['sgst']
                    items_dict[str(i)] = {}
                    item = items_dict[str(i)]
                    item['item_name'] = form.cleaned_data['item_name']
                    item['description'] = form.cleaned_data['description']
                    item['hsn_no'] = form.cleaned_data['hsn_no']
                    item['price'] = price
                    item['quantity'] = quantity
                    item['cgst'] = cgst
                    item['sgst'] = sgst
                    before_tax_total = before_tax_total + (price * quantity)
                    gst_inclusive_price = calculate_gst(price, quantity, cgst, sgst)
                    after_tax_total = after_tax_total + gst_inclusive_price
                    item['gst_inclusive_price'] = gst_inclusive_price
            discount = extra_form.cleaned_data['discount']
            shipping = extra_form.cleaned_data['shipping']
            if discount is None:
                discount = 0
            if shipping is None:
                shipping = 0
            discounted_total = after_tax_total - discount
            grand_total = discounted_total + shipping       
            items_dict['discount'] = discount
            items_dict['shipping'] = shipping
            items_dict['before_tax_total'] = before_tax_total
            items_dict['after_tax_total'] = after_tax_total
            items_dict['discounted_total'] = discounted_total
            items_dict['grand_total'] = grand_total
            pprint(items_dict)

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


def item_test(request):
    if request.method == 'POST':
        formset = ItemsFormset(request.POST)
        if formset.is_valid():
            print('formset is valid')
            for form in formset:
                if form.is_valid():
                    print(['FORMS'])
                    
                    
    else:
        formset = ItemsFormset()
    
    context = {
        'item_formset':formset
    }
    return render(request, 'base/itemform.html', context)
