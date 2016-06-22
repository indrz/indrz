#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from django.http import HttpResponse


from rest_framework.decorators import api_view
from rest_framework.response import Response

from buildings.models import Campus, Building, BuildingFloorSpace, BuildingFloor
from buildings.serializers import (CampusSerializer,
                                   BuildingSerializer,
                                   BuildingShortSerializer,
                                   BuildingFloorSpaceSerializer,
                                   BuildingFloorSerializer,
                                   SpaceSerializer,
                                   )

logger = logging.getLogger(__name__)

@api_view(['GET', ])
def campus_list(request, format=None):
    """
    List all buildings without details

    """

    if request.method == 'GET':
        campus = Campus.objects.all()
        serializer = CampusSerializer(campus, many=True)
        return Response(serializer.data)


@api_view(['GET', ])
def building_short_list(request, format=None):
    """
    List all buildings without details
    """
    if request.method == 'GET':
        buildings = Building.objects.all()
        serializer = BuildingShortSerializer(buildings, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = BuildingSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def list_buildings_on_campus(request, pk_campus):
    """
    List all buildings, located on a specific campus area
    """
    if request.method == 'GET':
        buildings = Building.objects.filter(fk_campus=pk_campus)
        serializer = BuildingSerializer(buildings, many=True)

        return Response(serializer.data)


@api_view(['GET', 'POST'])
def building_list(request, format=None):
    """
    List all buildings, or create a new building.
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
    Retrieve, update or delete a code snippet.
    """
    try:
        building = Building.objects.get(pk=pk)
    except Building.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BuildingSerializer(building)
        return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = BuildingSerializer(building, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # elif request.method == 'DELETE':
    #     building.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def building_floors_list(request, building_id, format=None):
    """
    List all floor ids for a specific building
    """
    if request.method == 'GET':
        floor_ids = BuildingFloor.objects.filter(fk_building=building_id)
        serializer = BuildingFloorSerializer(floor_ids, many=True)
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
def space_details(request, spaces_id, format=None):
    """
    Return the GeoJSON of a single space ex. a single room
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(id=spaces_id)
        serializer = SpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_space_by_name(request, building_id, space_name, format=None):
    """
    Return the GeoJSON of a single space passing your local space name
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(short_name=space_name, fk_building_id=building_id)
        serializer = SpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_external_id(request, building_id, external_room_id, format=None):
    """
    Return the GeoJSON of a single space passing your local room id we call it external id
    """
    if request.method == 'GET':
        floor_space_info = BuildingFloorSpace.objects.filter(room_external_id=external_room_id, fk_building_id=building_id)
        serializer = SpaceSerializer(floor_space_info, many=True)
        return Response(serializer.data)
