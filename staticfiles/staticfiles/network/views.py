from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VlanForm
from .models import Vlan

@login_required
def vlan_view(request):
    template_name = 'vlan_form.html'

    if request.method == 'GET':
        form = VlanForm()
        existing_vlans = Vlan.objects.filter(user=request.user)
        return render(request, template_name, {'form': form, 'existing_vlans': existing_vlans})

    elif request.method == 'POST':
        form = VlanForm(request.POST)
        existing_vlans = Vlan.objects.all()
        if form.is_valid():
            form.save()
            return redirect('network:vlan_view')

        return render(request, template_name, {'form': form, 'existing_vlans': existing_vlans})

@login_required
def vlan_delete_view(request, pk):
    if request.method == 'POST':
        vlan = Vlan.objects.get(pk=pk)
        vlan.delete()
    
    return redirect('network:vlan_view')
