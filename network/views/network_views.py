from ..models import Vlan, Network, Address
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse


@login_required
def network_view(request):
    # view de gestion de la page network
    template_name = 'network_form.html'

    if request.method == 'GET':
        networks_masks = Network.objects.all().order_by('mask')
        # selection des vlans non associés à un reseau et appartenant a l'utilisateur connecté
        availableVlans = Vlan.objects.filter(
            address__isnull=True,
            user=request.user
        ).order_by('vlan_id')
        
        # Vérifier si availableVlans est vide
        if not availableVlans:
            message = "Aucun VLAN disponible ou non associé à un réseau."
        else:
            message = None
        return render(request, template_name, {'networks_masks': networks_masks, 'availableVlans': availableVlans, 'message': message})
    
    elif request.method == 'POST':
        first_three_bytes_value = request.POST.get('first_three_bytes')
        nb_hosts = request.POST.get('nb_hosts_value')
        first_byte_network_range = request.POST.get('networkRange')
        selected_vlan = Vlan.objects.get(vlan_id=request.POST.get('vlans'), user=request.user)

        # premiere adresse : adresse de reseau
        address = Address()
        address.user = request.user
        address.vlan = selected_vlan
        address.ip = first_three_bytes_value + "." + str(int(first_byte_network_range))
        address.description = "adresse de reseau"
        address.save()
        
        address.description = ""
        for i in range (int(first_byte_network_range) + 1, int(first_byte_network_range) + int(nb_hosts) - 1):
            address = Address()
            address.user = request.user
            address.vlan = selected_vlan
            address.ip = first_three_bytes_value + "." + str(i)
            address.save()
        
        # derniere adresse : adresse de diffusion
        address = Address()
        address.user = request.user
        address.vlan = selected_vlan
        address.ip = first_three_bytes_value + "." + str(int(first_byte_network_range) + int(nb_hosts) - 1)
        address.description = "adresse de diffusion"
        address.save()

        return redirect('network:network_view')
            
    return render(request, template_name)

@login_required
def check_ip_in_db(request):
    # renvoi False si le range testé contient une IP présente dans la DB
    first_three_bytes = request.GET.get('firstThreeBytes')
    network_first_byte = request.GET.get('networkFirstByte')
    network_last_byte = request.GET.get('networkLastByte')

    ip_exists = False

    for current_byte in range(int(network_first_byte), int(network_last_byte) + 1):
        current_ip = f"{first_three_bytes}.{current_byte}"

        if Address.objects.filter(ip=current_ip).exists():
            ip_exists = True
            break

    return JsonResponse({'ip_exists': ip_exists})
