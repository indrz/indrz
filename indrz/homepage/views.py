import re
import json

from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.contrib.gis.db.models.functions import Centroid, AsGeoJSON

from rest_framework.decorators import api_view
from rest_framework.response import Response

from buildings.models import BuildingFloorSpace
from buildings.models import BuildingFloor

from geojson import Feature

from homepage.serializer import CampusFloorSerializer
from poi_manager.models import PoiCategory
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def view_map(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':
        map_name = kwargs.pop('map_name', None)
        building_id, = request.GET.get('buildingid', 1),
        campus_id = request.GET.get('campus', 1),
        space_id, = request.GET.get('spaceid', 0),
        zoom_level, = request.GET.get('zlevel', 17),
        route_from, = request.GET.get('startstr', ''),
        route_to, = request.GET.get('endstr', ''),
        centerx, = request.GET.get('centerx', 0),
        centery, = request.GET.get('centery', 0),
        floor_num, = request.GET.get('floor', 0),
        poi_name, = request.GET.get('poi-name', ''),
        search_text, = request.GET.get('q', ''),
        poi_id, = request.GET.get('poi-id', 0),
        share_xy = request.GET.get('search', ''),
        hide_left_menu = request.GET.get('hide-left', 'false')
        hide_top = request.GET.get('hide-top', 'false')
        hide_footer = request.GET.get('hide-footer', 'false')
        floor_num = int(floor_num)

        if floor_num == 0:
            floor_num = floor_num + 1
        else:
            floor_num = floor_num + 1

        if isinstance(centerx, str):
            if ',' in centerx:
                centerx = float(centerx.replace(',', '.'))
                centery = float(centery.replace(',', '.'))

        context.update({
            'map_name': map_name,
            'building_id': building_id,
            'campus_id': campus_id,
            'space_id': int(space_id),
            'zoom_level': zoom_level,
            'route_from': route_from,
            'route_to': route_to,
            'centerx': centerx,
            'centery': centery,
            'floor_num': int(floor_num),
            'poi_name' : poi_name,
            'search_text': search_text,
            'poi_id' : poi_id,
            'share_xy' : share_xy,
            'hide_top' : hide_top,
            'hide_left': hide_left_menu,
            'hide_footer' : hide_footer,
            'nodes': PoiCategory.objects.filter(enabled=True),
        })

    return render(request, context=context, template_name='map.html')


@api_view(['GET'])
def get_room_center(request, big_pk, format=None):
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    ip_addr = get_client_ip(request)
    # print('this is my IP : ' + ip_addr)

    if ip_addr.startswith('127.0.'):
        # if q.keys().index('searchString') < 0:
        #     raise Exception("Couldn't find AKS in parameter q")

        # searchString = q['searchString'].upper()
        searchString = big_pk.upper()

        if re.match('(\d{3}_\d{2}_[A-Z]{1}[A-Z0-9]{1}[0-9]{2}_\d{6})', searchString):
            re_is_match = "yes"
        else:
            raise Exception("input search string does not match AKS form zb 001_10_OG05_111200 or 001_10_U101_111900 ")

        # dont allow empty searchString, too short searchString or too long searchString (50 characters is way too much
        #  and probably a sql attack so we prevent it here aswell
        if searchString == "" or len(searchString) < 10 or len(searchString) > 20:
            raise Exception("searchString is too short. Must be at least 2 characters")

        # check for possible sql attacks etc...
        if '}' in searchString or '{' in searchString or ';' in searchString:
            raise Exception("illegal characters in searchString")

        space_qs = BuildingFloorSpace.objects.filter(room_external_id=big_pk)

        if space_qs:
            att = space_qs.values()[0]

            if att['multi_poly']:
                att['multi_poly'] = None

            centroid_res = BuildingFloorSpace.objects.annotate(json=AsGeoJSON(Centroid('multi_poly'))).get(
                room_external_id=big_pk).json

            res = Feature(geometry=json.loads(centroid_res), properties=att)

            return Response(res)
        else:
            return Response(
                {'error': 'Sorry we did not find any record in our database matching your id = ' + str(big_pk)})
    else:
        # raise Exception("wrong IP! your ip is : " + ip_addr)
        # return HttpResponseForbidden()
        raise PermissionDenied


@api_view(['GET'])
def get_campus_floors(request, campus_id, format=None):
    """
    Get a list of floors on campus
    """
    if request.method == 'GET':
        floor_list = BuildingFloor.objects.filter(fk_building=1)

        data = CampusFloorSerializer(floor_list, many=True)

        return Response(data.data)


def view_help(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':

        return render(request, template_name='hilfe.html')
