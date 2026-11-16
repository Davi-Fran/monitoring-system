from django.db import models

class FunctionChoices(models.TextChoices):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    LUMINOSITY = "luminosity"
    COUNT = "count"


class MeasurementUnitChoices(models.TextChoices):
    CELSIUS = "°C"
    PERCENT = "%"
    LUX = "lux"
    UNIT = "un"


UNIT_BY_FUNCTION = {
    FunctionChoices.TEMPERATURE: MeasurementUnitChoices.CELSIUS,
    FunctionChoices.HUMIDITY: MeasurementUnitChoices.PERCENT,
    FunctionChoices.LUMINOSITY: MeasurementUnitChoices.LUX,
    FunctionChoices.COUNT: MeasurementUnitChoices.UNIT,
}