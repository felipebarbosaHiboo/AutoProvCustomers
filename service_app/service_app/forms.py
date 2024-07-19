from django import forms

SERVICE_CHOICES = (
    ("1", "DIA STATIC BGP WITH VLAN_ID"),
    ("2", "DIA STATIC BGP"),
    ("3", "DIA STATIC"),
    ("4", "L2VPN ELAN"),
    ("5", "L2VPN ELINE"),
    ("6", "L3VPN BGP"),
    ("7", "L3VPN STATIC"),
)

class CustomerForm(forms.Form):
    customer_ID = forms.IntegerField()
    service_ID = forms.IntegerField()
    service_Type = forms.ChoiceField(choices=SERVICE_CHOICES)

class DiaStaticBgpWithVlanId_ServiceForm(forms.Form):
    interfaceName = forms.CharField()
    svlan = forms.IntegerField(max_value=4096)
    dataCenter = forms.CharField()
    cir = forms.IntegerField()
    cbs = forms.IntegerField()

