from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from poi_manager.models import PoiCategory, Poi, PoiIcon

class PoiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fk_poi_category', 'fk_building')
    search_fields = ('name', 'fk_building',)
    list_filter = ('fk_poi_category', 'fk_building')

admin.site.register(Poi, PoiAdmin)
admin.site.register(PoiIcon)
admin.site.register(PoiCategory, MPTTModelAdmin)