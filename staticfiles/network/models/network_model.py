# models/network_model.py
from django.db import models
from django.core.validators import validate_ipv4_address
from .vlan_model import Vlan


class Network(models.Model):
    """
    describe networks
    """
    id = models.AutoField(primary_key=True,unique=True)
    vlan = models.ForeignKey(Vlan, on_delete=models.CASCADE)
    description = models.CharField(max_length=32, null=True, blank=True)
    network_mask = models.CharField(max_length=15, validators=[validate_ipv4_address])
    network_address = models.CharField(max_length=15, validators=[validate_ipv4_address])
    network_broadcast = models.CharField(max_length=15, validators=[validate_ipv4_address])

    def __str__(self):
        return f"{self.nom} - {self.adresse_reseau}"