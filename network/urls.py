from django.urls import path
from .views import vlan_view, vlan_delete_view, menu_view, network_view, address_view, check_ip_in_db, get_network_addresses

app_name = 'network'
urlpatterns = [
    path('vlan/', vlan_view, name='vlan_view'),
    path('vlan/delete/<int:pk>/', vlan_delete_view, name='vlan_delete_view'),
    path('menu/', menu_view, name='menu_view'),
    path('network', network_view, name='network_view'),
    path('address', address_view, name='address_view'),
    path('checkIpInDb/', check_ip_in_db, name='checkIpInDb'),
    # exemple d'url pour test : http://127.0.0.1:8000/network/getNetworkAddresses/?vlan_id=20
    path('getNetworkAddresses/', get_network_addresses, name='getNetworkAddresses'),
]
