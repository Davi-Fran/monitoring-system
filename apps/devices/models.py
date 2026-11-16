from django.db import models
from django.utils import timezone

from apps.laboratories.models import Laboratory
from apps.devices.validators import mac_address_validator

class MicroControllerModel(models.Model):
    mcm_id = models.AutoField(primary_key=True)
    mcm_name = models.CharField(max_length=50)
    mcm_is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"MicroController Model #{self.mcm_id}:{self.mcm_name}"

    class Meta:
        db_table = "app_micro_controller_model"


class MicroController(models.Model):
    mc_id = models.AutoField(primary_key=True)
    mc_mac_address = models.CharField(
        max_length=17, 
        unique=True, 
        validators=[mac_address_validator]
    )
    mc_latitude = models.DecimalField(max_digits=10, decimal_places=8)
    mc_longitude = models.DecimalField(max_digits=11, decimal_places=8)
    mc_registered_at = models.DateTimeField(default=timezone.now)
    mc_model = models.ForeignKey(
        MicroControllerModel,
        related_name="mcm_devices",
        on_delete=models.PROTECT
    )
    mc_laboratory = models.ForeignKey(
        Laboratory,
        related_name="lab_installed_mcs",
        on_delete=models.PROTECT
    )
    mc_is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"MicroController #{self.mc_id}:{self.mc_mac_address}"

    class Meta:
        db_table = "app_micro_controller"