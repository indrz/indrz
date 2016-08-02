#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from buildings.models import Campus, Building, BuildingFloorSpace, BuildingFloor
from buildings.serializers import (CampusSerializer,
                                   BuildingSerializer,
                                   BuildingSerializerDetails,
                                   BuildingFloorSpaceSerializer,
                                   BuildingFloorGeomSerializer,
                                   SpaceSerializer,
                                   SpacesOnFloor,
                                   )

logger = logging.getLogger(__name__)


@api_view(['GET', ])
def campus_list(request, format=None):
    """
    List of campuses belonging to an organization

    """

    if request.method == 'GET':
        campus = Campus.objects.all()
        serializer = CampusSerializer(campus, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_campus_info(request, campus_id, format=None):
    """
    Get a list of buildings on a singlge campus
    """
    if request.method == 'GET':
        buildings_on_campus = Building.objects.filter(fk_campus=campus_id).order_by('id')
        serializer = BuildingSerializer(buildings_on_campus, many=True)
        return Response(serializer.data)


@api_view(['GET', ])
def list_buildings_on_campus(request, campus_id, format=None, **kwargs):
    """
    List all buildings within a single campus
    :param request:
    :param campus_id: integer
    :param format:
    :param kwargs: ?details=True   returns floor data aswell
    :return:
    """
    if request.method == 'GET':
        buildings = Building.objects.filter(fk_campus=campus_id).order_by('id')
        serializer = BuildingSerializer(buildings, many=True)

        map_name = kwargs.pop('map_name', None)
        details = request.GET.get('details')
        print(str(details))
        if details == 'True':
            serializer_detail = BuildingSerializer(buildings, many=True)
            return Response(serializer_detail.data)

        else:
            return Response(serializer.data)


@api_view(['GET', ])
def building_short_list(request, campus_id, format=None):
    """
    List all buildings without details
    """
    if request.method == 'GET':
        buildings = Building.objects.filter(fk_campus=campus_id)
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def building_list(request, format=None):
    """
    List all buildings in the system on every campus
    """
    if request.method == 'GET':
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

        # elif request.method == 'POST':
        #     serializer = BuildingSerializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def building_detail(request, pk, format=None):
    """
    Return all floors
    """
    try:
        building = Building.objects.get(pk=pk)
    except Building.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BuildingSerializer(building)
        return Response(serializer.data)


@api_view(['GET'])
def building_floors_list(request, building_id, format=None):
    """
    List all floor ids for a specific building
    """
    if request.method == 'GET':
        floor_ids = BuildingFloor.objects.filter(fk_building=building_id)
        serializer = BuildingFloorGeomSerializer(floor_ids, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_floor_info(request, building_id, floor_id, format=None):
    """
    Get data for a single floor by passing the building floor_id
    """

    if request.method == 'GET':
        floor_ids = BuildingFloor.objects.filter(fk_building=building_id)
        floor_data = floor_ids.filter(pk=floor_id)
        serializer = BuildingFloorGeomSerializer(floor_data, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def get_spaces_on_floor(request, floor_id, format=None):
    """
    List all spaces on the provided building and floor
    """
    if request.method == 'GET':

        space_ids = BuildingFloorSpace.objects.filter(fk_building_floor=floor_id)

        serializer = SpacesOnFloor(space_ids, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_building_floor_spaces(request, building_id, floor_id, format=None):
    """
    Return GeoJson of all spaces located on specified floor
    """

    if request.method == 'GET':
        floor_ids = BuildingFloor.objects.filter(fk_building=building_id)

        foo = BuildingFloorSpace.objects.filter(fk_building_floor=floor_ids)

        spaces_on_floor = BuildingFloorSpace.objects.filter(fk_building_floor=floor_id)

        serializer = BuildingFloorSpaceSerializer(spaces_on_floor, many=True, context={'request': request})
        return Response(serializer.data)



@api_view(['GET'])
def get_space_by_id(request, building_id, floor_id, space_id, format=None):
    """
    Provided a space id return GeoJson of that single space
    """
    if request.method == 'GET':
        space_value = BuildingFloorSpace.objects.filter(pk=space_id)
        serializer = BuildingFloorSpaceSerializer(space_value, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_space_by_name(request, building_id, floor_id, space_name, format=None):
    """
    Get information about a single space providing, building_id, floor_id, space_id
    """
    if request.method == 'GET':
        floor_ids = BuildingFloor.objects.filter(fk_building=building_id, fk_building_floor=floor_id)
        serializer = BuildingFloorGeomSerializer(floor_ids, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def building_spaces_list(request, building_id, floor_id, format=None):
    """
    List all spaces on a specified floor in given building.
    """
    if request.method == 'GET':
        floor_spaces = BuildingFloorSpace.objects.filter(fk_building=building_id, fk_building_floor=floor_id)
        serializer = BuildingFloorSpaceSerializer(floor_spaces, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def space_details(request, space_id, format=None):
    """
    Return the GeoJSON of a single space ex. a single room
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(id=space_id)
        serializer = BuildingFloorSpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_space_by_name(request, building_id, floor_id, space_name, format=None):
    """
    Return the GeoJSON of a single space passing your local space name
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(short_name=space_name, fk_building_id=building_id, fk_building_floor=floor_id)
        serializer = SpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_external_id(request, building_id, external_room_id, format=None):
    """
    Return the GeoJSON of a single space passing your local room id we call it external id
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(room_external_id=external_room_id,
                                                             fk_building_id=building_id)
        serializer = SpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)
