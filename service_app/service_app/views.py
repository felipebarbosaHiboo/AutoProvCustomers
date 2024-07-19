#views.py

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import (
    DiaStaticBgpWithVlanIdServiceForm, DiaStaticBgpServiceForm, DiaStaticServiceForm,
    L2vpnElanServiceForm, L2vpnElineServiceForm, L3vpnBgpServiceForm, L3vpnStaticServiceForm, DiaDynamicServiceForm,
    CustomerForm
)

def get_additional_fields(request):
    service_type = request.GET.get('service_type')
    html = ''
    if service_type == "1":  # DIA DYNAMIC
        form = DiaDynamicServiceForm()
    elif service_type == "2":  # DIA STATIC BGP WITH VLAN_ID
        form = DiaStaticBgpWithVlanIdServiceForm()
    elif service_type == "3":  # DIA STATIC BGP
        form = DiaStaticBgpServiceForm()
    elif service_type == "4":  # DIA STATIC
        form = DiaStaticServiceForm()
    elif service_type == "5":  # L2VPN ELAN
        form = L2vpnElanServiceForm()
    elif service_type == "6":  # L2VPN ELINE
        form = L2vpnElineServiceForm()
    elif service_type == "7":  # L3VPN BGP
        form = L3vpnBgpServiceForm()
    elif service_type == "8":  # L3VPN STATIC
        form = L3vpnStaticServiceForm()

    html = render_to_string('additional_fields.html', {'form': form})
    return JsonResponse({'html': html})

def customer(request):
    customer_form = CustomerForm(request.POST or None)
    additional_form = None  # Initialize the variable

    if request.method == 'POST':
        if customer_form.is_valid():
            customer_ID = customer_form.cleaned_data['customer_ID']
            print('Customer ID', customer_ID)
            service_ID = customer_form.cleaned_data['service_ID']
            print('Service ID', service_ID)
            service_Type = customer_form.cleaned_data['service_Type']
            print('Service Type', service_Type)

            if service_Type == "1":  # DIA DYNAMIC
                additional_form = DiaDynamicServiceForm(request.POST)
            elif service_Type == "2":  # DIA STATIC BGP WITH VLAN_ID
                additional_form = DiaStaticBgpWithVlanIdServiceForm(request.POST)
            elif service_Type == "3":  # DIA STATIC BGP
                additional_form = DiaStaticBgpServiceForm(request.POST)
            elif service_Type == "4":  # DIA STATIC
                additional_form = DiaStaticServiceForm(request.POST)
            elif service_Type == "5":  # L2VPN ELAN
                additional_form = L2vpnElanServiceForm(request.POST)
            elif service_Type == "6":  # L2VPN ELINE
                additional_form = L2vpnElineServiceForm(request.POST)
            elif service_Type == "7":  # L3VPN BGP
                additional_form = L3vpnBgpServiceForm(request.POST)
            elif service_Type == "8":  # L3VPN STATIC
                additional_form = L3vpnStaticServiceForm(request.POST)

            if additional_form and additional_form.is_valid():
                # Process additional form data
                print('Additional Form Data:', additional_form.cleaned_data)

    context = {
        'customer_form': customer_form,
        'additional_form': additional_form,
    }
    return render(request, "forms.html", context)
