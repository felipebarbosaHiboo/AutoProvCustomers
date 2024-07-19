import os
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings
from django import forms

from .forms import (
    DiaStaticBgpWithVlanIdServiceForm, DiaStaticBgpServiceForm, DiaStaticServiceForm,
    L2vpnElanServiceForm, L2vpnElineServiceForm, L3vpnBgpServiceForm, L3vpnStaticServiceForm, DiaDynamicServiceForm,
    CustomerForm
)

TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'templates', 'service_templates')

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
    config_script = ""

    if request.method == 'POST':
        if customer_form.is_valid():
            customer_ID = customer_form.cleaned_data['customer_ID']
            service_ID = customer_form.cleaned_data['service_ID']
            service_Type = customer_form.cleaned_data['service_Type']

            form_data = {}
            if service_Type == "1":  # DIA DYNAMIC
                additional_form = DiaDynamicServiceForm(request.POST)
                template_filename = 'dia_dynamic.txt'
            elif service_Type == "2":  # DIA STATIC BGP WITH VLAN_ID
                additional_form = DiaStaticBgpWithVlanIdServiceForm(request.POST)
                template_filename = 'dia_static_bgp_with_vlanid.txt'
            elif service_Type == "3":  # DIA STATIC BGP
                additional_form = DiaStaticBgpServiceForm(request.POST)
                template_filename = 'dia_static_bgp.txt'
            elif service_Type == "4":  # DIA STATIC
                additional_form = DiaStaticServiceForm(request.POST)
                template_filename = 'dia_static.txt'
            elif service_Type == "5":  # L2VPN ELAN
                additional_form = L2vpnElanServiceForm(request.POST)
                template_filename = 'l2vpn_elan.txt'
            elif service_Type == "6":  # L2VPN ELINE
                additional_form = L2vpnElineServiceForm(request.POST)
                template_filename = 'l2vpn_eline.txt'
            elif service_Type == "7":  # L3VPN BGP
                additional_form = L3vpnBgpServiceForm(request.POST)
                template_filename = 'l3vpn_bgp.txt'
            elif service_Type == "8":  # L3VPN STATIC
                additional_form = L3vpnStaticServiceForm(request.POST)
                template_filename = 'l3vpn_static.txt'

            if additional_form and additional_form.is_valid():
                form_data = additional_form.cleaned_data
                config_script = generate_config_script(template_filename, form_data)

                # Ensure the media directory exists
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

                # Save to file
                script_filename = f"service_customer_{form_data['cust_id']}_service_{form_data['svc_id']}.txt"
                script_filepath = os.path.join(settings.MEDIA_ROOT, script_filename)
                with open(script_filepath, 'w') as script_file:
                    script_file.write(config_script)

                return render(request, "forms.html", {
                    'customer_form': customer_form,
                    'additional_form': additional_form,
                    'config_script': config_script,
                    'script_filename': script_filename,
                    'script_filepath': script_filepath
                })

    context = {
        'customer_form': customer_form,
        'additional_form': additional_form,
    }
    return render(request, "forms.html", context)

def generate_config_script(template_filename, data):
    template_filepath = os.path.join(TEMPLATE_DIR, template_filename)
    with open(template_filepath, 'r') as template_file:
        template = template_file.read()
    for key, value in data.items():
        template = template.replace(f"${{{key.replace('_', '-')}}}", str(value))
    return template
