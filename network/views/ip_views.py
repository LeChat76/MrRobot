from django.shortcuts import render
from ping3 import ping, verbose_ping
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import Vlan, Address
from django.http import JsonResponse


@login_required
def get_free_ip_addresses(request):
    # renvoi les adresses IP non affectées par rapport à un vlan donné    
    selected_vlan_id = request.GET.get('vlan_id')
    network_addresses = Address.objects.filter(vlan__vlan_id=selected_vlan_id, user=request.user, hostname='', description='')

    data = [{'id': address.id, 'ip': address.ip} for address in network_addresses]

    return JsonResponse(data, safe=False)

@login_required
def donne_ip(request):
    message = None

    # Sélection des vlans associés à un réseau et appartenant à l'utilisateur connecté
    availableVlans = Vlan.objects.filter(
        address__isnull=False,
        user=request.user
    ).order_by('vlan_id').distinct()

    # verification si aucun vlan disponible
    if not availableVlans:
        message = "Aucun VLAN disponible ou aucun VLAN associé à un réseau."

    if request.method == "POST":

        selected_vlan = request.POST.get('selectedVlan', None)
        address = Address.objects.get(id=request.POST.get('addressId'))

        ping_from_host = 'pingFromHost' in request.POST
        ping_from_server = 'pingFromServer' in request.POST

        if ping_from_host:
            if faire_ping_depuis_hote(address):
                message='Reponse au ping, adresse utilisée, selectionnez une autre adresse.'
                return render(request, 'ip_form.html', {'availableVlans': availableVlans, 'selected_vlan': selected_vlan, 'message': message})
            
        if ping_from_server:
            if faire_ping_depuis_serveur(address):
                message='Reponse au ping, adresse utilisée, selectionnez une autre adresse.'
                return render(request, 'ip_form.html', {'availableVlans': availableVlans, 'selected_vlan': selected_vlan, 'message': message})
        
        address.hostname = request.POST.get('hostname')
        address.description = request.POST.get('description')
        address.save()

        return render(request, 'ip_form.html', {'availableVlans': availableVlans, 'selected_vlan': selected_vlan, 'message': message})

    # print("SELECTED_VLAN_ID :", selected_vlan_index)
    return render(request, 'ip_form.html', {'availableVlans': availableVlans, 'message': message})

def faire_ping_depuis_hote(address):
    result = ping(address.ip)
    return result

def faire_ping_depuis_serveur(address):
    result = ping(address.ip)
    return result

