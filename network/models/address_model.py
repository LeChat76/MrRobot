# models/address_model.py
from django.db import models
from django.conf import settings
from django.core.validators import validate_ipv4_address
from .network_model import Vlan


class Address(models.Model):
    """
    describe all IP addresses assign to an network
    """
    ip = models.CharField(primary_key=True, unique=True, max_length=15, validators=[validate_ipv4_address])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    vlan = models.ForeignKey(Vlan, on_delete=models.CASCADE, blank=True, null=True)
    hostname = models.CharField(max_length=63, null=True, blank=True)
    description = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        unique_together = ['user', 'ip']
