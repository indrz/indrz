from django.conf.urls import url
from poi_manager.views import poi_category_list, add_category, poi_category_json, poi_by_name, poi_list,\
    poi_category_by_name, get_poi_by_cat_name, get_poi_by_id, get_poicat_by_id

urlpatterns = [
               url(r'^category-list/$', poi_category_list, name='category-list'),
               url(r'^category-poi/$', poi_category_json, name='category-json'),
    
               url(r'^list/$', poi_list, name='list all pois'),
               url(r'^(?P<poi_id>\d{0,6})/$', get_poi_by_id, name='get poi by id'),

               url(r'^category/(?P<cat_id>\d{1,6})/$', get_poicat_by_id, name='get poi category'),
               url(r'^category/(?P<category_name>.+)/$', poi_category_by_name, name='list categories by name'),

               url(r'^name/(?P<category_name>.+)/$', get_poi_by_cat_name, name='search_poi_by_category'),

               url(r'^add_category/$', add_category, name='add_category'),  # NEW MAPPING!
               url(r'^search/(?P<poi_name>.+)', poi_by_name, name='poi by name')

]

# urlpatterns = format_suffix_patterns(urlpatterns)
