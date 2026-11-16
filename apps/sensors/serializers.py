from rest_framework import serializers

from apps.sensors.models import SensorModel, Sensor, SensorReading
from apps.devices.serializers import MicroControllerDetailSerializer

OFFLINE_DEFAULT_MINUTES = 60
OFFLINE_MAX_MINUTES = 43200

class SensorModelSerializer(serializers.ModelSerializer):    
    class Meta:
        model = SensorModel
        fields = "__all__"
        extra_kwargs = {
            "sm_measurement_unit": {"read_only": True}
        }



class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"

    def validate_sen_model(self, value):
        if not value.sm_is_active:
            raise serializers.ValidationError("This selected sensor model is inactive!")
        
        return value

    def validate_sen_connected_to(self, value):
        if not value.mc_is_active:
            raise serializers.ValidationError("The selected micro controller is inactive!")

        return value

class SensorDetailSerializer(serializers.ModelSerializer):
    sen_model = SensorModelSerializer()
    sen_connected_to = MicroControllerDetailSerializer()

    class Meta:
        model = Sensor
        fields = "__all__"

class OfflineSensorSerializer(serializers.Serializer):
    sensor_id = serializers.IntegerField(source="sen_id")
    sensor_model = serializers.CharField(source="sen_model.sm_name")
    function = serializers.CharField(source="sen_model.sm_function")
    micro_controller_id = serializers.IntegerField(source="sen_connected_to.mc_id")
    mac_address = serializers.CharField(source="sen_connected_to.mc_mac_address")
    laboratory = serializers.CharField(source="sen_connected_to.mc_laboratory.lab_name")
    last_measured_at = serializers.DateTimeField(allow_null=True)

class OfflineSensorQuerySerializer(serializers.Serializer):
    minutes = serializers.IntegerField(
        required=False,
        default=OFFLINE_DEFAULT_MINUTES,
        min_value=1,
        max_value=OFFLINE_MAX_MINUTES,
    )



class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = "__all__"

    def validate_sr_sen(self, value):
        if not value.sen_is_active:
            raise serializers.ValidationError("The selected sensor is inactive!")

        return value

class LatestReadingSerializer(serializers.Serializer):
    sensor_id = serializers.IntegerField(source="sen_id")
    sensor_model = serializers.CharField(source="sen_model.sm_name")
    function = serializers.CharField(source="sen_model.sm_function")
    measurement_unit = serializers.CharField(source="sen_model.sm_measurement_unit")
    reading_id = serializers.IntegerField(source="latest_reading_id", allow_null=True)
    measured_value = serializers.DecimalField(
        source="latest_measured_value",
        max_digits=12,
        decimal_places=2,
        allow_null=True,
    )
    measured_at = serializers.DateTimeField(
        source="latest_measured_at",
        allow_null=True,
    )

class LatestReadingQuerySerializer(serializers.Serializer):
    last_24h = serializers.BooleanField(required=False, default=False)