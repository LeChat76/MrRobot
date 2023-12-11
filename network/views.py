from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
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
        existing_vlans = Vlan.objects.filter(user=request.user)

        try:
            if form.is_valid():
                vlan = form.save(commit=False)
                vlan.user = request.user
                vlan.save()
                return redirect('network:vlan_view')
        except IntegrityError:
            # Contrainte d'unicité violée, affichage d'un message d'erreur
            form.add_error('number', 'Ce numéro de VLAN existe déjà.')

        return render(request, template_name, {'form': form, 'existing_vlans': existing_vlans})

@login_required
def vlan_delete_view(request, pk):
    vlan = Vlan.objects.filter(pk=pk, user=request.user)

    if request.method == 'POST':
        vlan.delete()
        return redirect('network:vlan_view')

    return render(request, 'vlan_delete.html', {'vlan': vlan})
