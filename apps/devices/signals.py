from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.devices.models import MicroController
from apps.laboratories.models import Laboratory

@receiver(post_save, sender=Laboratory)
def desactivate_micro_controllers_of_inactivated_laboratories(sender, instance, **kwargs):
    if instance.lab_is_active:
        return

    MicroController.objects.filter(
        mc_laboratory=instance,
        mc_is_active=True
    ).update(mc_is_active=False)