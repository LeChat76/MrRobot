from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    Customize user table
    """
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        """
        just for the pluralisation and FR translation, perfection is perfection you know!  ;-)
        """
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
