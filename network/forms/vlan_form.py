from django import forms
from ..models import Vlan

class VlanForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'maxlength': 255}))
    class Meta:
        model = Vlan
        fields = ['id', 'name', 'description']
