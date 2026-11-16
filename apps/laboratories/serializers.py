from rest_framework import serializers

from apps.laboratories.models import Laboratory

class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = "__all__"


class LaboratoryMicroControllerSerializer(serializers.Serializer):
    mc_id = serializers.IntegerField()
    mc_mac_address = serializers.CharField()
    mc_latitude = serializers.DecimalField(max_digits=10, decimal_places=8)
    mc_longitude = serializers.DecimalField(max_digits=11, decimal_places=8)
    mc_registered_at = serializers.DateTimeField()
    mc_is_active = serializers.BooleanField()


class LaboratoryDetailSerializer(serializers.ModelSerializer):
    lab_installed_mcs = LaboratoryMicroControllerSerializer(many=True)
    
    class Meta:
        model = Laboratory
        fields = "__all__"