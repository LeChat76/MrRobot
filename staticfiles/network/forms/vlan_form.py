from django import forms
from ..models import Vlan

class VlanForm(forms.ModelForm):
    id = forms.IntegerField(min_value=2, max_value=4095, required=False)
    name = forms.CharField(max_length=32, required=False)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': 255}),
        required=False
    )
    class Meta:
        model = Vlan
        fields = [
            'id',
            'name',
            'description'
        ]
