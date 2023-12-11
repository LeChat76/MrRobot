# models/address_model.py
from django.db import models
from django.core.validators import validate_ipv4_address
from .network_model import Network


class Address(models.Model):
    """
    describe all IP addresses assign to an network
    """
    ip = models.CharField(primary_key=True, unique=True, max_length=15, validators=[validate_ipv4_address])
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    description = models.CharField(max_length=32, null=True, blank=True)
