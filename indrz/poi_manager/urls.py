from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from poi_manager.views import poi_category_list, add_category

urlpatterns = [url(r'^category-list/$', poi_category_list, name='category-list'),
               url(r'^category/(?P<category_name_slug>[\w\-]+)/$', poi_category_list, name='category'),
               # New!
               url(r'^add_category/$', add_category, name='add_category'),  # NEW MAPPING!

               ]

urlpatterns = format_suffix_patterns(urlpatterns)
