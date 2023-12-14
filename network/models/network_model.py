# models/network_model.py
from django.db import models
from django.core.validators import validate_ipv4_address, MaxValueValidator
from .vlan_model import Vlan


class Network(models.Model):
    """
    describe networks
    """
    id = models.AutoField(primary_key=True,unique=True)
    vlan_id = models.ForeignKey(Vlan, on_delete=models.CASCADE, blank=True, null=True)
    mask = models.CharField(max_length=15, validators=[validate_ipv4_address])
    CIDR = models.IntegerField(default=0, validators=[MaxValueValidator(32)], unique=True)
    nb_hosts = models.IntegerField(default=0, unique=True)

    # def __str__(self):
    #     return f"{self.nom} - {self.adresse_reseau}"