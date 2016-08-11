from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from routing.views import create_route_from_coords, create_route_from_id, create_route_from_search, \
    force_route_mid_point
from buildings.views import get_spaces_on_floor, campus_list, list_buildings_on_campus, campus_search, space_details
from api.views import autocomplete_list

urlpatterns = [
    #  ex valid call from to  /api/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2
    # url(r'^directions/(?P<start_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<start_floor>\d+)&(?P<end_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<end_floor>\d+)&(?P<route_type>[0-9])/$', 'create_route', name='directions'),

    # url(r'^spaces/search/(?P<search_term>[a-zA-Z0-9]{2,5})/$', 'autocomplete_list', name='spaces_list'),
    url(r'^spaces/search/$', autocomplete_list, name='spaces_list'),

    # url(r'^directions/(?P<building_name>building=d{1,5})&start={1,6}&destination={1,6}/$', 'route_room_to_room', name='route-space-to-space' )

]

# SPACES API URLS
urlpatterns += [
    # url(r'^spaces/$', 'spaces_list', name='list_all_campuses'),
    url(r'^spaces/(?P<space_id>\d{1,5})/$', space_details, name='show_space_details'),
    # url(r'^spaces/(?P<building_id>\d{1,5})/(?P<floor_id>\d{1,5})/$', 'building_spaces_list',
    #                         name='building_spaces_list'),
    # url(r'^spaces/(?P<space_name>.+)/$', 'get_space_by_name', name='get_space_by_name'),
]

# Floors API URLS
urlpatterns += [
    url(r'^floors/(?P<floor_id>\d{1,5})/$', get_spaces_on_floor, name='get_spaces_on_floor'),
    # url(r'^spaces/(?P<space_name>.+)/$', 'get_space_by_name', name='get_space_by_name'),
]

# CAMPUS AND BUILDINGS API URLS
urlpatterns += [
    url(r'^campus/$', campus_list, name='list_all_campuses'),
    url(r'^campus/(?P<campus_id>\d{1,5})/$', campus_buildings_list, name='campus_building_list'),
    url(r'^campus/(?P<campus_id>\d{1,5})/shortlist/$', campus_buildings_short_list, name='buildings_list'),
    url(r'^campus/(?P<campus_id>\d{1,5})/search/(?P<search_string>.{1,60})', campus_search, name='search_campus'),
    url(r'^buildings/', include('buildings.urls')),

    ]

urlpatterns += [

    url(r'^library/', include('homepage.library.urls')),

    ]


# DIRECTIONS API URLS
urlpatterns += [
    url(
        r'^directions/(?P<start_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<start_floor>[-]?\d+)&(?P<end_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<end_floor>[-]?\d+)&(?P<route_type>[0-9])/$',
        create_route_from_coords, name='root_coords'),
    # url(r'^directions/(?P<start_room_key>\d{5})&(?P<end_room_key>\d{5})&(?P<route_type>[0-9])/$', 'route_room_to_room', name='route-room-to-room'),
    url(
        r'^directions/(?P<building_id>buildingid=\d{1,5})&(?P<start_room_id>startid=\d{1,5})&(?P<end_room_id>endid=\d{1,5})(?P<route_type>&type=\d{1,5})?/$',
        create_route_from_id, name='routing-from-id'),
    url(
        r'^directions/(?P<building_id>buildingid=\d{1,5})&(?P<start_term>startid=.+)&(?P<end_term>endid=.+)(?P<route_type>&type=\d{1,5})?/$',
        create_route_from_search, name='routing-from-search'),
    url(r'^directions/force_mid/', force_route_mid_point, name='force-route-midpoint')
]

# http://localhost:8000/api/v1/directions/force_mid/?startnode=1385&midnode=1167&endnode=1252
# http://localhost:8000/api/v1/directions/buildingid=1&startid=307: Orne&endid=311: Mayenne
# http://localhost:8000/api/v1/directions/buildingid=1&startid=1173&endid=1231

urlpatterns = format_suffix_patterns(urlpatterns)
