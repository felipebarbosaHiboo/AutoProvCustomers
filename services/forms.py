from django import forms
from django.core.exceptions import ValidationError
import re

# Mixin for adding Bootstrap CSS classes
class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')
            if field_name == 'cbs':
                field.widget.attrs['readonly'] = True

    def add_error(self, field, error):
        super().add_error(field, error)
        self.fields[field].widget.attrs['class'] += ' is-invalid'

# Validators for IPv4 and IPv6 with Mask
def validate_ipv4_with_mask(value):
    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$', value):
        raise ValidationError('Enter a valid IPv4 address with a mask (e.g., 192.168.0.1/24).')

def validate_ipv6_with_mask(value):
    if not re.match(r'^([0-9a-fA-F:]+)/\d{1,3}$', value):
        raise ValidationError('Enter a valid IPv6 address with a mask (e.g., 2001:db8::/32).')

# Common Choices
SERVICE_CHOICES = [
    ("0", "SELECT ONE AND CLICK SAVE"),
    ("1", "DIA DYNAMIC"),
    ("2", "DIA STATIC BGP WITH VLAN_ID"),
    ("3", "DIA STATIC BGP"),
    ("4", "DIA STATIC"),
    ("5", "L2VPN ELAN"),
    ("6", "L2VPN ELINE"),
    ("7", "L3VPN BGP"),
    ("8", "L3VPN STATIC"),
]

CIR_CHOICES = [(f"{x}m", f"{x} Mbps") for x in (100, 200, 300, 400, 500)] + \
              [(f"{x}g", f"{x} Gbps") for x in (1, 2, 3, 4, 5, 10, 100)]

# Base Service Form with Common Fields and cbs Calculation
class BaseServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=0, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=0, label="Service ID", initial=1234)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) * (1000 if cir.endswith('g') else 1)
            cleaned_data["cbs"] = cir_value * 0.1
        return cleaned_data

# Mixin for IPv4 and IPv6 Address Fields
class IPAddressMixin(forms.Form):
    prefix_ipv4 = forms.CharField(
        label="IPv4 Network/Mask",
        initial="10.10.10.10/8",
        validators=[validate_ipv4_with_mask],
        widget=forms.TextInput(attrs={
            'pattern': r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$',
            'title': 'Enter a valid IPv4 address with a mask (e.g., 192.168.0.1/24).'
        })
    )
    addr_ipv4_pe = forms.CharField(
        label="IPv4 Address/Mask PE",
        initial="10.10.10.10/8",
        validators=[validate_ipv4_with_mask],
        widget=forms.TextInput(attrs={
            'pattern': r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$',
            'title': 'Enter a valid IPv4 address with a mask (e.g., 192.168.0.1/24).'
        })
    )
    addr_ipv4_ce = forms.CharField(
        label="IPv4 Address CE",
        initial="10.10.10.10/8",
        validators=[validate_ipv4_with_mask],
        widget=forms.TextInput(attrs={
            'pattern': r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$',
            'title': 'Enter a valid IPv4 address with a mask (e.g., 192.168.0.1/24).'
        })
    )
    prefix_ipv6 = forms.CharField(
        label="IPv6 Address/Mask",
        initial="2001:db8::1/32",
        validators=[validate_ipv6_with_mask]
    )
    addr_ipv6_pe = forms.CharField(
        label="IPv6 Address/Mask PE",
        initial="2001:db8::1/32",
        validators=[validate_ipv6_with_mask]
    )
    addr_ipv6_ce = forms.CharField(
        label="IPv6 Address/Mask CE",
        initial="2001:db8::1/32",
        validators=[validate_ipv6_with_mask]
    )


# Specific Forms
class CustomerForm(forms.Form, BootstrapMixin):
    service_Type = forms.ChoiceField(choices=SERVICE_CHOICES)

class DiaDynamicServiceForm(BaseServiceForm):
    svlan = forms.IntegerField(max_value=4096, min_value=1, label="Service VLAN ID", initial=4096)
    pwht_dc = forms.ChoiceField(choices=[('dc01', 'DC01'), ('dc02', 'DC02')], label="Data Center")

class DiaStaticBgpWithVlanIdServiceForm(BaseServiceForm, IPAddressMixin):
    cust_asn = forms.IntegerField(label="Autonomous System Number", initial=65000)
    vlan_id = forms.IntegerField(max_value=4096, min_value=1, label="VLAN ID", initial=1245)
    ifu = forms.IntegerField(label="Unit Number", initial=0)
    auth_key = forms.CharField(label="Authentication Key", initial="Key negotiated with customer")

class DiaStaticBgpServiceForm(BaseServiceForm, IPAddressMixin):
    cust_asn = forms.IntegerField(label="Autonomous System Number", initial=65000)

class DiaStaticServiceForm(BaseServiceForm, IPAddressMixin):
    pass

class L2vpnElanServiceForm(BaseServiceForm):
    mtu = forms.ChoiceField(choices=[('1522', '1522'), ('9216', '9216')], label="MTU")
    vpls_pref = forms.ChoiceField(choices=[('primary', 'Primary'), ('backup', 'Backup')], label="VPLS Multi-Homing Preference")
    vpls_site_id = forms.IntegerField(label="VPLS Site Identifier", initial=1121)

class L2vpnElineServiceForm(BaseServiceForm):
    mtu = forms.ChoiceField(choices=[('1522', '1522'), ('9216', '9216')], label="MTU")
    vpws_id_local = forms.IntegerField(label="Local VPWS Circuit ID", initial=104100)
    vpws_id_remote = forms.IntegerField(label="Remote VPWS Circuit ID", required=False)

    def clean(self):
        cleaned_data = super().clean()
        vpws_id_local = cleaned_data.get("vpws_id_local")
        if vpws_id_local:
            str_id = str(vpws_id_local)
            cleaned_data["vpws_id_remote"] = int(str_id[3:] + str_id[:3])
        return cleaned_data

class L3vpnBgpServiceForm(BaseServiceForm, IPAddressMixin):
    cust_asn = forms.IntegerField(label="Autonomous System Number", initial=65000)

class L3vpnStaticServiceForm(BaseServiceForm, IPAddressMixin):
    pass
