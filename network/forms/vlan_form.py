from django import forms
from ..models import Vlan

class VlanForm(forms.ModelForm):
    class Meta:
        model = Vlan
        fields = ['id', 'name', 'description']
