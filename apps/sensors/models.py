from django.db import models
from django.utils import timezone

from apps.devices.models import MicroController
from apps.sensors.validators import validate_not_in_future
from apps.sensors.choices import FunctionChoices, MeasurementUnitChoices

class SensorModel(models.Model):
    sm_id = models.AutoField(primary_key=True)
    sm_name = models.CharField(max_length=50)
    sm_function = models.CharField(
        max_length=11,
        choices=FunctionChoices.choices
    )
    sm_measurement_unit = models.CharField(
        max_length=3,
        choices=MeasurementUnitChoices.choices
    )
    sm_is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"Sensor Model #{self.sm_id}:{self.sm_name}"

    class Meta:
        db_table = "app_sensor_model"


class Sensor(models.Model):
    sen_id = models.AutoField(primary_key=True)
    sen_model = models.ForeignKey(
        SensorModel,
        related_name="sm_installed_sensors",
        on_delete=models.PROTECT,
    )
    sen_connected_to = models.ForeignKey(
        MicroController,
        related_name="mc_connected_sensors",
        on_delete=models.PROTECT,
    )
    sen_is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Sensor #{self.sen_id}~{self.sen_model.sm_function}"

    class Meta:
        db_table = "app_sensor"


class SensorReading(models.Model):
    sr_id = models.BigAutoField(primary_key=True)
    sr_measured_value = models.DecimalField(max_digits=12, decimal_places=2)
    sr_measured_at = models.DateTimeField(
        default=timezone.now,
        validators=[validate_not_in_future]
    )
    sr_sen = models.ForeignKey(
        Sensor,
        related_name="sen_readings",
        on_delete=models.PROTECT,
    )


    def __str__(self):
        return f"Sensor reading #{self.sr_id} in {self.sr_measured_at}"

    class Meta:
        db_table = "app_sensor_reading"
        indexes = [
            models.Index(
                fields=["sr_measured_at"],
                name="idx_sr_measured_at",
            )
        ]