from rest_framework import serializers
from buildings.models import Campus, Building, BuildingFloorSpace, LtSpaceType, BuildingFloor
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class CampusSerializer(serializers.ModelSerializer):
    buildings = serializers.StringRelatedField(many=True)

    class Meta:
        model = Campus
        fields = ('id', 'campus_name', 'description', 'fk_organization', 'buildings')
        # depth = 1  # include organization information


# class ItemSerializer(serializers.ModelSerializer):
#     category_name = serializers.RelatedField(source='category', read_only=True)
#
#     class Meta:
#         model = Item
#         fields = ('id', 'name', 'category_name')


class BuildingFloorSpaceSerializer(GeoFeatureModelSerializer):
    building_name = serializers.StringRelatedField(source='fk_building', read_only=True)
    floor_name = serializers.StringRelatedField(source='fk_building_floor', read_only=True)
    type_name = serializers.StringRelatedField(source='space_type', read_only=True)

    class Meta:
        model = BuildingFloorSpace
        geo_field = "multi_poly"
        fields = ('id', 'short_name', 'floor_num', 'multi_poly', 'fk_building', 'fk_building_floor',
                  'room_external_id', 'space_type', 'building_name', 'floor_name', 'type_name')

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




class SpaceSerializer(GeoFeatureModelSerializer):
    fk_building = BuildingSerializer(read_only=True)
    fk_building_floor = BuildingFloorGeomSerializer(read_only=True)

    class Meta:
        model = BuildingFloorSpace
        geo_field = "multi_poly"
        fields = ('id', 'short_name', 'floor_num', 'multi_poly', 'fk_building', 'fk_building_floor',
                  'room_external_id', 'space_type')
