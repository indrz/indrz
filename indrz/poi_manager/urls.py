from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from poi_manager.views import poi_category_list, add_category, poi_category_json, poi_by_name, poi_list,\
    poi_category_by_name, get_poi_by_category

urlpatterns = [
               url(r'^category-list/$', poi_category_list, name='category-list'),
               url(r'^category-poi/$', poi_category_json, name='category-json'),
               url(r'^list/$', poi_list, name='list all pois'),
               url(r'^category/(?P<category_name>.+)/$', poi_category_by_name, name='list categories by name'),
               url(r'^name/(?P<category_name>.+)/$', get_poi_by_category, name='search_poi_by_category'),

               url(r'^add_category/$', add_category, name='add_category'),  # NEW MAPPING!

               url(r'^search/(?P<poi_name>.+)', poi_by_name, name='poi by name')

]

# urlpatterns = format_suffix_patterns(urlpatterns)
