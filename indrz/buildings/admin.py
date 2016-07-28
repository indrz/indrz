from django.contrib import admin
from django.contrib.gis import admin as gis_admin

from buildings.models import LtAccessType, LtSpaceType, LtCondition
from buildings.models import  Organization, Campus, Building
from buildings.models import  BuildingFloor, BuildingFloorSpace, InteriorFloorSection

admin.site.register(Organization, gis_admin.OSMGeoAdmin)
admin.site.register(Campus, gis_admin.OSMGeoAdmin)
admin.site.register(InteriorFloorSection, gis_admin.OSMGeoAdmin)

class LtSpaceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('name',)


class BuildingFloorSpaceAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('short_name', 'room_external_id', 'room_number', 'fk_building_floor', 'floor_num', 'space_type', 'id')
    search_fields = ('short_name', 'fk_building')


class BuildingFloorAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('short_name', 'fk_building', 'id')
    search_fields = ('short_name',)


class BuildingAdmin(gis_admin.OSMGeoAdmin):
    list_display = ('building_name',  'fk_campus', 'fk_organization', 'id')
    search_fields = ('building_name', 'fk_campus')


admin.site.register(LtAccessType)
admin.site.register(LtSpaceType, LtSpaceTypeAdmin)
admin.site.register(LtCondition)

admin.site.register(Building, BuildingAdmin )
admin.site.register(BuildingFloor, BuildingFloorAdmin )
admin.site.register(BuildingFloorSpace, BuildingFloorSpaceAdmin)