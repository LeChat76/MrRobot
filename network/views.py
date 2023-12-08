from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .forms import VlanForm
from .models import Vlan
from django.views import View

class VlanView(View):
    template_name = 'vlan_form.html'

    def get(self, request):
        form = VlanForm()
        existing_vlans = Vlan.objects.all()
        return render(request, self.template_name, {'form': form, 'existing_vlans': existing_vlans})

    def post(self, request):
        form = VlanForm(request.POST)
        existing_vlans = Vlan.objects.all()
        if form.is_valid():
            form.save()
            return redirect('network:VlanView')

        return render(request, self.template_name, {'form': form, 'existing_vlans': existing_vlans})
    
class VlanDeleteView(DeleteView):
    model = Vlan
    template_name = 'vlan_delete.html'
    success_url = reverse_lazy('network:VlanView') 
