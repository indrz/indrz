from rest_framework import serializers

from poi_manager.models import Poi, PoiCategory
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class PoiSerializer(GeoFeatureModelSerializer):


    class Meta:
        model = Poi
        geo_field = 'geom'
        depth = 1
        fields = ('id', 'name', 'floor_num', 'fk_poi_category')


class PoiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoiCategory
        # fields = ('floor_num', 'short_name')