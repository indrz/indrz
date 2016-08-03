from rest_framework import serializers
from buildings.models import Campus, Building, BuildingFloorSpace, LtSpaceType, BuildingFloor
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class CampusSerializer(serializers.ModelSerializer):
    buildings = serializers.StringRelatedField(many=True)

    class Meta:
        model = Campus
        fields = ('id', 'campus_name', 'description', 'fk_organization', 'buildings')
        # depth = 1  # include organization information



class BuildingFloorSpaceSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = BuildingFloorSpace
        geo_field = "multi_poly"
        fields = ('id', 'short_name', 'floor_num', 'multi_poly', 'fk_building', 'fk_building_floor',
                  'room_external_id', 'space_type')


class BuildingFloorGeomSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = BuildingFloor
        geo_field = 'multi_poly'
        fields = ('id', 'short_name', 'floor_num', 'fk_building')


class FloorSerializer(serializers.ModelSerializer):
    buildingfloorspace_set = BuildingFloorSpaceSerializer(many=True, read_only=True)

    class Meta:
        model = BuildingFloor
        fields = ('id', 'short_name', 'floor_num', 'fk_building', 'buildingfloorspace_set')


class BuildingSerializer(serializers.ModelSerializer):

    buildingfloor_set = FloorSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = ('id', 'building_name', 'num_floors', 'fk_organization', 'fk_campus', 'buildingfloor_set')


class BuildingShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ('id', 'building_name', 'num_floors', 'fk_organization', 'fk_campus')


class FloorSerializerDetails(serializers.ModelSerializer):

    buildingfloorspace_set = BuildingFloorSpaceSerializer(many=True, read_only=True)

    class Meta:
        model = BuildingFloor
        fields = ('id', 'short_name', 'floor_num', 'fk_building', 'buildingfloorspace_set')


class BuildingSerializerDetails(serializers.ModelSerializer):

    buildingfloor_set = FloorSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = ('id', 'building_name', 'num_floors', 'buildingfloor_set')


class SpacesOnFloor(GeoFeatureModelSerializer):

    class Meta:
        model = BuildingFloorSpace
        geo_field = "multi_poly"
        fields = ('id', 'short_name', 'floor_num', 'fk_building',
                  'room_external_id')


class SpaceSerializer(GeoFeatureModelSerializer):
    fk_building = BuildingSerializer(read_only=True)
    fk_building_floor = BuildingFloorGeomSerializer(read_only=True)

    class Meta:
        model = BuildingFloorSpace
        geo_field = "multi_poly"
        fields = ('id', 'short_name', 'floor_num', 'multi_poly', 'fk_building', 'fk_building_floor',
                  'room_external_id', 'space_type')
