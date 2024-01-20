from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Vlan, Address
from ..forms import AddressForm
from django.http import JsonResponse


@login_required
def get_network_addresses(request):
    # renvoi les adresses IP associées à un vlan

    selected_vlan_id = request.GET.get('vlan_id')
    network_addresses = Address.objects.filter(vlan__vlan_id=selected_vlan_id, user=request.user)

    data = [{'id': address.id, 'ip': address.ip, 'hostname': address.hostname, 'description': address.description} for address in network_addresses]

    return JsonResponse(data, safe=False)

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
            message = "Aucun VLAN disponible ou aucun VLAN associé à un réseau."

    return render(request, template_name, {'form': form, 'availableVlans': availableVlans, 'network_addresses': network_addresses, 'message': message})

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
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=405)