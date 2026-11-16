from rest_framework import serializers

from apps.devices.models import MicroControllerModel, MicroController
from apps.laboratories.serializers import LaboratorySerializer

class MicroControllerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroControllerModel
        fields = "__all__"


class MicroControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroController
        fields = "__all__"

    def validate_mc_model(self, value):
        if not value.mcm_is_active:
            raise serializers.ValidationError("The selected micro controller model is inactive!")

        return value

    def validate_mc_laboratory(self, value):
        if not value.lab_is_active:
            raise serializers.ValidationError("The selected laboratory is inactive!")
            
        return value


class MicroControllerDetailSerializer(serializers.ModelSerializer):
    mc_model = MicroControllerModelSerializer()
    mc_laboratory = LaboratorySerializer()
    
    class Meta:
        model = MicroController
        fields = "__all__"