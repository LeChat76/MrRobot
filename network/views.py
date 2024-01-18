from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import VlanForm, AddressForm
from .models import Vlan, Network, Address

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
    
@login_required
def menu_view(request):
    return render(request, 'network_menu.html')

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
            message = "Aucun VLAN disponible.<br>Allez en créer d'autres ou supprimez des réseaux associés."
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
def address_view(request):
    template_name = 'address_form.html'
    form = AddressForm()
    network_addresses = []
    message = None

    # Sélection des vlans associés à un réseau et appartenant à l'utilisateur connecté
    availableVlans = Vlan.objects.filter(
        address__isnull=False,
        user=request.user
    ).order_by('vlan_id').distinct()

    if request.method == 'GET':
        # Obtenir le VLAN sélectionné (s'il existe)
        selected_vlan_id = request.GET.get('vlans')

        if selected_vlan_id:
            # Obtenir les adresses réseau associées au VLAN sélectionné
            network_addresses = Address.objects.filter(vlan__vlan_id=selected_vlan_id)

    # verification si aucun vlan disponible
    if not availableVlans:
        if request.method == 'GET':
            message = "Aucun VLAN disponible. Allez en créer d'autres ou supprimez des réseaux associés."

    return render(request, template_name, {'form': form, 'availableVlans': availableVlans, 'network_addresses': network_addresses, 'message': message})

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

@login_required
def get_network_addresses(request):
    # renvoi les adresses IP associées à un vlan

    selected_vlan_id = request.GET.get('vlan_id')
    network_addresses = Address.objects.filter(vlan__vlan_id=selected_vlan_id, user=request.user)

    data = [{'id': address.id, 'ip': address.ip, 'hostname': address.hostname, 'description': address.description} for address in network_addresses]

    return JsonResponse(data, safe=False)

@login_required
def modify_address(request):
    # modifie les valeurs des champs d'une address dans la table address
    if request.method == "POST":
        addressId = request.POST.get('addressId')
        hostname = request.POST.get('hostname')
        description = request.POST.get('description')
        address = Address.objects.get(id=addressId)
        address.hostname = hostname
        address.description = description
        address.save()
        return JsonResponse({'success': True, 'message': 'Données mises à jour avec succès'})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

@login_required
def donne_ip(request):
    template_name = 'ip_form.html'
    # form = AddressForm()
    # network_addresses = []
    message = None

    # Sélection des vlans associés à un réseau et appartenant à l'utilisateur connecté
    availableVlans = Vlan.objects.filter(
        address__isnull=False,
        user=request.user
    ).order_by('vlan_id').distinct()

    # verification si aucun vlan disponible
    if not availableVlans:
        # if request.method == 'GET':
            message = "Aucun VLAN disponible. Allez en créer d'autres ou supprimez des réseaux associés."

    return render(request, template_name, {'availableVlans': availableVlans, 'message': message})

@login_required
def get_free_ip_addresses(request):
    # renvoi les adresses IP non affectées par rapport à un vlan donné    
    selected_vlan_id = request.GET.get('vlan_id')
    network_addresses = Address.objects.filter(vlan__vlan_id=selected_vlan_id, user=request.user, hostname='', description='')

    data = [{'id': address.id, 'ip': address.ip} for address in network_addresses]

    # print("DATA", data)

    return JsonResponse(data, safe=False)