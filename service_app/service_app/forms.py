import re

from django import forms
from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError
import re

class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = None
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'cbs':
                field.widget.attrs['readonly'] = True

    def add_error(self, field, error):
        super().add_error(field, error)
        self.fields[field].widget.attrs['class'] += ' is-invalid'

def validate_ipv4_with_mask(value):
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$')
    if not pattern.match(value):
        raise ValidationError('Enter a valid IPv4 address with a mask (e.g., 192.168.0.1/24).')

def validate_ipv6_with_mask(value):
    pattern = re.compile(r'^([0-9a-fA-F:]+)\/\d{1,3}$')
    if not pattern.match(value):
        raise ValidationError('Enter a valid IPv6 address with a mask (e.g., 2001:db8::/32).')

SERVICE_CHOICES = (
    ("0", "SELECT ONE AND CLICK SAVE"),
    ("1", "DIA DYNAMIC"),
    ("2", "DIA STATIC BGP WITH VLAN_ID"),
    ("3", "DIA STATIC BGP"),
    ("4", "DIA STATIC"),
    ("5", "L2VPN ELAN"),
    ("6", "L2VPN ELINE"),
    ("7", "L3VPN BGP"),
    ("8", "L3VPN STATIC"),
)

CIR_CHOICES = [
    ("100m", "100 Mbps"),
    ("200m", "200 Mbps"),
    ("300m", "300 Mbps"),
    ("400m", "400 Mbps"),
    ("500m", "500 Mbps"),
    ("1g", "1 Gbps"),
    ("2g", "2 Gbps"),
    ("3g", "3 Gbps"),
    ("4g", "4 Gbps"),
    ("5g", "5 Gbps"),
    ("10g", "10 Gbps"),
    ("100g", "100 Gbps"),
]

class CustomerForm(forms.Form, BootstrapMixin):
    service_Type = forms.ChoiceField(choices=SERVICE_CHOICES)

class DiaDynamicServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID", initial=1234)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    svlan = forms.IntegerField(max_value=4096, min_value=1, label="Service VLAN ID", initial=4096)
    pwht_dc = forms.ChoiceField(choices=[('dc01', 'DC01'), ('dc02', 'DC02')], label="Data Center")
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) if cir.endswith('m') else int(cir[:-1]) * 1000
            cleaned_data["cbs"] = cir_value * 0.1
        return cleaned_data

class DiaStaticBgpWithVlanIdServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID", initial=1234)
    cust_asn = forms.IntegerField(label="Autonomous System Number", initial=65000)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    vlan_id = forms.IntegerField(max_value=4096, min_value=1, label="VLAN ID", initial=1245)
    ifu = forms.IntegerField(label="Unit Number", initial=0)
    prefix_ipv4_01 = forms.CharField(label="IPv4 Network/Mask 1", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    prefix_ipv4_02 = forms.CharField(label="IPv4 Network/Mask 2", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_pe_rpm = forms.CharField(label="IPv4 Address PE RPM", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_ce1 = forms.CharField(label="IPv4 Address CE1", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_ce2 = forms.CharField(label="IPv4 Address CE2", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    prefix_ipv6 = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_pe_rpm = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_ce1 = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_ce2 = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)
    auth_key = forms.CharField(label="Authentication Key", initial="Key negotiated with customer")

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) if cir.endswith('m') else int(cir[:-1]) * 1000
            cleaned_data["cbs"] = cir_value * 0.1
        return cleaned_data

class DiaStaticBgpServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID", initial=1234)
    cust_asn = forms.IntegerField(label="Autonomous System Number", initial=65000)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    prefix_ipv4 = forms.CharField(label="IPv4 Network/Mask", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_ce = forms.CharField(label="IPv4 Address CE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    prefix_ipv6 = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_ce = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) if cir.endswith('m') else int(cir[:-1]) * 1000
            cleaned_data["cbs"] = cir_value * 0.1
        return cleaned_data

class DiaStaticServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID", initial=1234)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    prefix_ipv4 = forms.CharField(label="IPv4 Network/Mask", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_ce = forms.CharField(label="IPv4 Address CE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    prefix_ipv6 = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_ce = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) if cir.endswith('m') else int(cir[:-1]) * 1000
            cleaned_data["cbs"] = cir_value * 0.1
        return cleaned_data

class L2vpnElanServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID", initial=1234)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    mtu = forms.ChoiceField(choices=[('1522', '1522'), ('9216', '9216')], label="MTU")
    vpls_pref = forms.ChoiceField(choices=[('primary', 'Primary'), ('backup', 'Backup')], label="VPLS Multi-Homing Preference")
    vpls_site_id = forms.IntegerField(label="VPLS Site Identifier", initial=1121)
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) if cir.endswith('m') else int(cir[:-1]) * 1000
            cleaned_data["cbs"] = cir_value * 0.1
        return cleaned_data

class L2vpnElineServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID", initial=1234)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    mtu = forms.ChoiceField(choices=[('1522', '1522'), ('9216', '9216')], label="MTU")
    vpws_id_local = forms.IntegerField(label="Local VPWS Circuit ID", initial=104100)
    vpws_id_remote = forms.IntegerField(label="Remote VPWS Circuit ID", required=False)
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) if cir.endswith('m') else int(cir[:-1]) * 1000
            cleaned_data["cbs"] = cir_value * 0.1

        vpws_id_local = cleaned_data.get("vpws_id_local")
        if vpws_id_local:
            str_id = str(vpws_id_local)
            cleaned_data["vpws_id_remote"] = int(str_id[3:] + str_id[:3])

        return cleaned_data

class L3vpnBgpServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID", initial=1234)
    cust_asn = forms.IntegerField(label="Autonomous System Number", initial=65000)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    prefix_ipv4 = forms.CharField(label="IPv4 Network/Mask", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_ce = forms.CharField(label="IPv4 Address CE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    prefix_ipv6 = forms.GenericIPAddressField(protocol='IPv6', label="IPv6 Network/Mask", initial="2001:db8::/32")
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_ce = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) if cir.endswith('m') else int(cir[:-1]) * 1000
            cleaned_data["cbs"] = cir_value * 0.1
        return cleaned_data

class L3vpnStaticServiceForm(forms.Form, BootstrapMixin):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID", initial=123456)
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID", initial=1234)
    ifd = forms.CharField(label="Interface Name", initial="xe-0/0/0")
    prefix_ipv4 = forms.CharField(label="IPv4 Network/Mask", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    addr_ipv4_ce = forms.CharField(label="IPv4 Address CE", initial="10.10.10.10/8", validators=[validate_ipv4_with_mask])
    prefix_ipv6 = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    addr_ipv6_ce = forms.CharField(label="IPv6 Address/Mask PE", initial="2001:db8::1/32", validators=[validate_ipv6_with_mask])
    cir = forms.ChoiceField(choices=CIR_CHOICES, label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size", required=False)

    def clean(self):
        cleaned_data = super().clean()
        cir = cleaned_data.get("cir")
        if cir:
            cir_value = int(cir[:-1]) if cir.endswith('m') else int(cir[:-1]) * 1000
            cleaned_data["cbs"] = cir_value * 0.1
        return cleaned_data
