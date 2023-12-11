from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Vlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vlan_id = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=2, message='Le VLAN ID doit être supérieur à 1.'),
            MaxValueValidator(limit_value=4095, message='Le VLAN ID doit être inférieur à 4096.'),
        ]
    )
    name = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ['user', 'vlan_id']

    def __str__(self):
        return f"Vlan ID : {self.id} - Nom : {self.name}"
