from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import VlanForm
from ..models import Vlan
from django.db import IntegrityError


@login_required
def vlan_view(request):
    template_name = 'vlan_form.html'

    # accès à la page des vlans
    if request.method == 'GET':
        form = VlanForm()
        existing_vlans = Vlan.objects.filter(user=request.user).order_by('vlan_id')
        return render(request, template_name, {'form': form, 'existing_vlans': existing_vlans})

    # envoi d'un "submit" (click sur bouton "ajouter") depuis la page des vlans
    elif request.method == 'POST':
        form = VlanForm(request.POST)
        existing_vlans = Vlan.objects.filter(user=request.user).order_by('vlan_id')

        try:
            if form.is_valid():
                vlan = form.save(commit=False)
                vlan.user = request.user
                # si name est vide, ajout d'un nom du type "VLAN " & vlan_id
                if not form.cleaned_data['name']:
                    vlan.name = f"VLAN {form.cleaned_data['vlan_id']}"
                # ajout du vlan dans la DB
                vlan.save()

                #retour à la page des vlans
                return redirect('network:vlan_view')
            
        except IntegrityError:
            # Contrainte d'unicité violée, affichage d'un message d'erreur
            form.add_error('vlan_id', 'Ce numéro de VLAN existe déjà.')

        return render(request, template_name, {'form': form, 'existing_vlans': existing_vlans})

@login_required
def vlan_delete_view(request, pk):
    # selection du vlan à supprimer combiné à l'utilisateur connecté
    vlan = Vlan.objects.filter(pk=pk, user=request.user)

    if request.method == 'POST':
        vlan.delete()
        return redirect('network:vlan_view')
    
