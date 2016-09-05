from django.conf.urls import url

from routing.views import create_route_from_coords, create_route_from_id, create_route_from_search, \
    force_route_mid_point

urlpatterns = [
    url(
        r'(?P<start_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<start_floor>[-]?\d+)&(?P<end_coord>[-]?\d+\.?\d+,\d+\.\d+),(?P<end_floor>[-]?\d+)&(?P<route_type>[0-9])/$',
        create_route_from_coords, name='root_coords'),
    # url(r'^directions/(?P<start_room_key>\d{5})&(?P<end_room_key>\d{5})&(?P<route_type>[0-9])/$', 'route_room_to_room', name='route-room-to-room'),
    url(
        r'(?P<start_room_id>startid=\d{1,5})&(?P<end_room_id>endid=\d{1,5})(?P<route_type>&type=\d{1,5})?/$',
        create_route_from_id, name='routing-from-id'),
    url(
        r'(?P<start_term>startstr=.+)&(?P<end_term>endstr=.+)(?P<route_type>&type=\d{1,5})?/$',
        create_route_from_search, name='routing-from-search'),
    url(r'force_mid/', force_route_mid_point, name='force-route-midpoint')
]
