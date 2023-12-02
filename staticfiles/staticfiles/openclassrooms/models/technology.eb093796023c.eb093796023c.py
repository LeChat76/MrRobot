from django.db import models


class Technology(models.Model):
    """
    This class describe technologies used for an project
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        """
        just for the pluralisation and FR translation, perfection is perfection you know!  ;-)
        """
        verbose_name = "Technologie"
        verbose_name_plural = "Technologies"
