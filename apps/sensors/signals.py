from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.sensors.models import Sensor
from apps.devices.models import MicroController
from apps.laboratories.models import Laboratory

@receiver(post_save, sender=MicroController)
def desactivate_sensors_of_inactive_micro_controller(sender, instance, **kwargs):
    if instance.mc_is_active:
        return

    Sensor.objects.filter(
        sen_connected_to=instance,
        sen_is_active=True,
    ).update(sen_is_active=False)


@receiver(post_save, sender=Laboratory)
def desactivate_sensors_of_micro_controller_of_inactive_laboratory(sender, instance, **kwargs):
    if instance.lab_is_active:
        return

    micro_controllers = MicroController.objects.filter(mc_laboratory=instance)
    
    Sensor.objects.filter(
        sen_connected_to__in=micro_controllers,
        sen_is_active=True
    ).update(sen_is_active=False)