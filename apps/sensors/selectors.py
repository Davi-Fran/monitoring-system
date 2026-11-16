from datetime import timedelta

from django.db.models import OuterRef, Subquery, Max, Q
from django.utils import timezone

from apps.core.selectors import model_list

from apps.sensors.models import SensorModel, Sensor, SensorReading
from apps.sensors.filters import SensorModelFilterSet, SensorFilterSet, SensorReadingFilterSet


RECENT_READINGS_WINDOW = timedelta(hours=24)


# SENSOR MODEL METHODS
def sensor_model_list(*, filters=None):
    return model_list(
        queryset=SensorModel.objects.all(),
        filterset_class=SensorModelFilterSet,
        filters=filters,
        order_by_field="sm_name",
    )



# SENSOR METHODS
def sensor_list(*, filters=None):
    return model_list(
        queryset=Sensor.objects.all(),
        filterset_class=SensorFilterSet,
        filters=filters,
        order_by_field="sen_id",
    )

def sensor_retrieve():
    return model_list(
        queryset=Sensor.objects.select_related("sen_model", "sen_connected_to"),
        filterset_class=SensorFilterSet,
    )



# SENSOR READING METHODS
def sensor_reading_list(*, filters=None):
    return model_list(
        queryset=SensorReading.objects.all(),
        filterset_class=SensorReadingFilterSet,
        filters=filters,
        order_by_field="sr_id",
    )



# BUSINESS RULES & EXTRAS
def latest_reading_list(*, last_24h=False):
    latest_reading = SensorReading.objects.filter(sr_sen=OuterRef("pk"))

    if last_24h:
        since = timezone.now() - RECENT_READINGS_WINDOW
        latest_reading = latest_reading.filter(sr_measured_at__gte=since)

    latest_reading = latest_reading.order_by("-sr_measured_at", "-sr_id")

    sensors = (
        Sensor.objects
        .select_related("sen_model")
        .annotate(
            latest_reading_id=Subquery(latest_reading.values("sr_id")[:1]),
            latest_measured_value=Subquery(latest_reading.values("sr_measured_value")[:1]),
            latest_measured_at=Subquery(latest_reading.values("sr_measured_at")[:1]),
        )
        .order_by("sen_id")
    )

    if last_24h:
        sensors = sensors.filter(latest_reading_id__isnull=False)

    return sensors


def offline_sensors_list(*, minutes):
    cutoff = timezone.now() - timedelta(minutes=minutes)

    return (
        Sensor.objects
        .filter(sen_is_active=True, sen_connected_to__mc_is_active=True)
        .select_related("sen_model", "sen_connected_to__mc_laboratory")
        .annotate(last_measured_at=Max("sen_readings__sr_measured_at"))
        .filter(Q(last_measured_at__lt=cutoff) | Q(last_measured_at__isnull=True))
        .order_by("last_measured_at")
    )