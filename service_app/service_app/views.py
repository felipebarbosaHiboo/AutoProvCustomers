from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import CustomerForm, DiaStaticBgpWithVlanId_ServiceForm

# Create your views here.

def get_additional_fields(request):
    service_type = request.GET.get('service_type')
    html = ''
    if service_type == "1":  # DIA STATIC BGP WITH VLAN_ID
        form = DiaStaticBgpWithVlanId_ServiceForm()
        html = render_to_string('additional_fields.html', {'form': form})
    return JsonResponse({'html': html})
def customer(request):
    customer_form = CustomerForm(request.POST or None)
    dia_static_bgp_with_vlanid_form = None

    if request.method == 'POST':
        if customer_form.is_valid():
            customer_ID = customer_form.cleaned_data['customer_ID']
            print('Customer ID', customer_ID)
            service_ID = customer_form.cleaned_data['service_ID']
            print('Service ID', service_ID)
            service_Type = customer_form.cleaned_data['service_Type']
            print('Service Type', service_Type)

            if service_Type == "1":  # DIA STATIC BGP WITH VLAN_ID
                dia_static_bgp_with_vlanid_form = DiaStaticBgpWithVlanId_ServiceForm(request.POST)
                if dia_static_bgp_with_vlanid_form.is_valid():
                    # Process DiaStaticBgpWithVlanId_ServiceForm data
                    print('Additional Form Data:', dia_static_bgp_with_vlanid_form.cleaned_data)

    context = {
        'customer_form': customer_form,
        'dia_static_bgp_with_vlanid_form': dia_static_bgp_with_vlanid_form,
    }
    return render(request, "forms.html", context)

