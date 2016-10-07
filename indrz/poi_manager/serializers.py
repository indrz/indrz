from rest_framework import serializers

from poi_manager.models import Poi, PoiCategory

class PoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        #fields = ('floor_num', 'short_name')


class PoiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoiCategory
        # fields = ('floor_num', 'short_name')