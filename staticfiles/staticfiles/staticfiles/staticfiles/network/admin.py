from django.contrib import admin
from .models import Vlan, Network, Address


class VlanAdmin(admin.ModelAdmin):
    """
    used to add column about vlan in django console admin
    """
    list_display = ('id', 'name', 'description')

class NetworkAdmin(admin.ModelAdmin):
    """
    used to add column about network in django console admin
    """
    list_display = ('vlan', 'network_address', 'network_broadcast', 'network_mask', 'description')

class AddressAdmin(admin.ModelAdmin):
    """
    used to add column about address in django console admin
    """
    list_display = ('ip', 'network', 'description',)

"""
tables to include in django administration page
"""
admin.site.register(Vlan, VlanAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Address, AddressAdmin)
