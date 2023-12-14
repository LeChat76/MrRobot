from django import forms
from ..models import Network


class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ['vlan_id', 'nb_hosts', 'mask', 'CIDR']