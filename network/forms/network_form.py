from django import forms
from ..models import Network, Vlan


class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ['vlan', 'nb_hosts', 'mask', 'CIDR']
