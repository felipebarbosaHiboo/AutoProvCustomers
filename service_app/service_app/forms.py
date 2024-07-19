from django import forms

SERVICE_CHOICES = (
    ("0", "SELECT ONE AND CLICK SAVE"),
    ("0", ""),
    ("1", "DIA DYNAMIC"),
    ("2", "DIA STATIC BGP WITH VLAN_ID"),
    ("3", "DIA STATIC BGP"),
    ("4", "DIA STATIC"),
    ("5", "L2VPN ELAN"),
    ("6", "L2VPN ELINE"),
    ("7", "L3VPN BGP"),
    ("8", "L3VPN STATIC"),
)

class CustomerForm(forms.Form):
    customer_ID = forms.IntegerField()
    service_ID = forms.IntegerField()
    service_Type = forms.ChoiceField(choices=SERVICE_CHOICES)

class DiaDynamicServiceForm(forms.Form):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID")
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID")
    ifd = forms.CharField(label="Interface Name")
    svlan = forms.IntegerField(max_value=4096, min_value=1, label="Service VLAN ID")
    pwht_dc = forms.ChoiceField(choices=[('dc01', 'DC01'), ('dc02', 'DC02')], label="Data Center")
    cir = forms.IntegerField(label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size")

class DiaStaticBgpWithVlanIdServiceForm(forms.Form):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID")
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID")
    cust_asn = forms.IntegerField(label="Autonomous System Number")
    ifd = forms.CharField(label="Interface Name")
    vlan_id = forms.IntegerField(max_value=4096, min_value=1, label="VLAN ID")
    ifu = forms.IntegerField(label="Unit Number")
    prefix_ipv4_01 = forms.CharField(label="IPv4 Network/Mask 1")
    prefix_ipv4_02 = forms.CharField(label="IPv4 Network/Mask 2")
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE")
    addr_ipv4_pe_rpm = forms.CharField(label="IPv4 Address PE RPM")
    addr_ipv4_ce1 = forms.CharField(label="IPv4 Address CE1")
    addr_ipv4_ce2 = forms.CharField(label="IPv4 Address CE2")
    prefix_ipv6 = forms.CharField(label="IPv6 Network/Mask")
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE")
    addr_ipv6_pe_rpm = forms.CharField(label="IPv6 Address PE RPM")
    addr_ipv6_ce1 = forms.CharField(label="IPv6 Address CE1")
    addr_ipv6_ce2 = forms.CharField(label="IPv6 Address CE2")
    cir = forms.IntegerField(label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size")
    auth_key = forms.CharField(label="Authentication Key")


class DiaStaticBgpServiceForm(forms.Form):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID")
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID")
    cust_asn = forms.IntegerField(label="Autonomous System Number")
    ifd = forms.CharField(label="Interface Name")
    prefix_ipv4 = forms.CharField(label="IPv4 Network/Mask")
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE")
    addr_ipv4_ce = forms.CharField(label="IPv4 Address CE")
    prefix_ipv6 = forms.CharField(label="IPv6 Network/Mask")
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE")
    addr_ipv6_ce = forms.CharField(label="IPv6 Address CE")
    cir = forms.IntegerField(label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size")

class DiaStaticServiceForm(forms.Form):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID")
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID")
    ifd = forms.CharField(label="Interface Name")
    prefix_ipv4 = forms.CharField(label="IPv4 Network/Mask")
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE")
    addr_ipv4_ce = forms.CharField(label="IPv4 Address CE")
    prefix_ipv6 = forms.CharField(label="IPv6 Network/Mask")
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE")
    addr_ipv6_ce = forms.CharField(label="IPv6 Address CE")
    cir = forms.IntegerField(label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size")

class L2vpnElanServiceForm(forms.Form):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID")
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID")
    ifd = forms.CharField(label="Interface Name")
    mtu = forms.ChoiceField(choices=[('1522', '1522'), ('9216', '9216')], label="MTU")
    vpls_pref = forms.ChoiceField(choices=[('primary', 'Primary'), ('backup', 'Backup')], label="VPLS Multi-Homing Preference")
    vpls_site_id = forms.IntegerField(label="VPLS Site Identifier")
    cir = forms.IntegerField(label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size")


class L2vpnElineServiceForm(forms.Form):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID")
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID")
    ifd = forms.CharField(label="Interface Name")
    mtu = forms.ChoiceField(choices=[('1522', '1522'), ('9216', '9216')], label="MTU")
    vpws_id_local = forms.IntegerField(label="Local VPWS Circuit ID")
    vpws_id_remote = forms.IntegerField(label="Remote VPWS Circuit ID")
    cir = forms.IntegerField(label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size")

class L3vpnBgpServiceForm(forms.Form):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID")
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID")
    cust_asn = forms.IntegerField(label="Autonomous System Number")
    ifd = forms.CharField(label="Interface Name")
    prefix_ipv4 = forms.CharField(label="IPv4 Network/Mask")
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE")
    addr_ipv4_ce = forms.CharField(label="IPv4 Address CE")
    prefix_ipv6 = forms.CharField(label="IPv6 Network/Mask")
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE")
    addr_ipv6_ce = forms.CharField(label="IPv6 Address CE")
    cir = forms.IntegerField(label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size")

class L3vpnStaticServiceForm(forms.Form):
    cust_id = forms.IntegerField(max_value=999999, min_value=100000, label="Customer ID")
    svc_id = forms.IntegerField(max_value=9999, min_value=1000, label="Service ID")
    ifd = forms.CharField(label="Interface Name")
    prefix_ipv4 = forms.CharField(label="IPv4 Network/Mask")
    addr_ipv4_pe = forms.CharField(label="IPv4 Address/Mask PE")
    addr_ipv4_ce = forms.CharField(label="IPv4 Address CE")
    prefix_ipv6 = forms.CharField(label="IPv6 Network/Mask")
    addr_ipv6_pe = forms.CharField(label="IPv6 Address/Mask PE")
    addr_ipv6_ce = forms.CharField(label="IPv6 Address CE")
    cir = forms.IntegerField(label="Committed Information Rate")
    cbs = forms.IntegerField(label="Committed Burst Size")