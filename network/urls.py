from django.urls import path
from .views import vlan_view, vlan_delete_view, menu_view, network_view

app_name = 'network'
urlpatterns = [
    path('vlan/', vlan_view, name='vlan_view'),
    path('vlan/delete/<int:pk>/', vlan_delete_view, name='vlan_delete_view'),
    path('menu/', menu_view, name='menu_view'),
    path('network', network_view, name='network_view'),
]
