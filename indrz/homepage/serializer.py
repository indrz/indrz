from rest_framework import serializers

from buildings.models import BuildingFloor

class CampusFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingFloor
        fields = ('floor_num', 'short_name')