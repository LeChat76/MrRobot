from django.contrib import admin
from .models import Vlan, Network, Address
from django.forms import TextInput
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class VlanAdmin(admin.ModelAdmin):
    """
    used to add column about vlan in django console admin
    """
    list_display = ('id', 'name', 'description')

class NetworkAdmin(admin.ModelAdmin):
    """
    used to add column about network in django console admin
    """
    list_display = ('mask', 'nb_hosts', 'CIDR')

    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'type': 'number', 'min': '1', 'max': '32'})},
    }

class AddressAdmin(admin.ModelAdmin):
    """
    used to add column about address in django console admin
    """
    list_display = ('ip', 'get_vlan_id', 'hostname', 'description',)

    def get_vlan_id(self, obj):
        return obj.vlan.vlan_id

    get_vlan_id.short_description = 'VLAN number'

"""
tables to include in django administration page
"""
admin.site.register(Vlan, VlanAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Address, AddressAdmin)
