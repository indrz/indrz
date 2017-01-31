#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import traceback
import logging
import json

import requests
from django.conf import settings
from django.http import HttpResponseNotFound
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geojson import loads, Feature, FeatureCollection

from poi_manager.models import Poi

from homepage.search_wu import search_any


logger = logging.getLogger(__name__)


def get_room_centroid_node(space_id):
    '''
    Find the room center point coordinates
    and find the closest route node point
    :param building_id: integer value of building
    :param space_id: internal space id as integer
    :return: Closest route node to submitted room number
    '''

    room_center_q = """SELECT  layer,
            ST_asGeoJSON(st_centroid(geom))
            AS geom FROM geodata.search_index_v
            WHERE id ={0};""".format(space_id)

    cur = connection.cursor()
    cur.execute(room_center_q)

    res = cur.fetchall()

    res2 = res[0]

    space_floor = res2[0]
    space_geom_x = json.loads(res2[1])
    space_geom_y = json.loads(res2[1])

    x_coord = float(space_geom_x['coordinates'][0])
    y_coord = float(space_geom_y['coordinates'][1])

    space_node_id = find_closest_network_node(x_coord, y_coord, space_floor)
    try:
        return space_node_id
    except:
        logger.error("error get room center " + str(space_node_id))
        logger.error(traceback.format_exc())
        return {'error': 'error get room center'}


def find_closest_network_node(x_coord, y_coord, floor):
    """
    Enter a given coordinate x,y and floor number and
    find the nearest network node id
    to start or end the route on
    :param x_coord: float  in epsg 3857
    :param y_coord: float  in epsg 3857
    :param floor: integer value equivalent to floor such as 2  = 2nd floor
    :return: node id as an integer
    """
    # connect to our Database
    # logger.debug("now running function find_closest_network_node")
    cur = connection.cursor()

    # find nearest node on network within 200 m
    # and snap to nearest node

    query = """ SELECT
        verts.id as id
        FROM geodata.networklines_3857_vertices_pgr AS verts
        INNER JOIN
          (select ST_PointFromText('POINT({0} {1} {2})', 3857)as geom) AS pt
        ON ST_DWithin(verts.the_geom, pt.geom, 50) and st_Z(verts.the_geom)={2}
        ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
        LIMIT 1;""".format(x_coord, y_coord, floor)


    cur.execute(query)

    # get the result
    query_result = cur.fetchone()

    # check if result is not empty
    if query_result is not None:
        # get first result in tuple response there is only one
        point_on_networkline = int(query_result[0])
        return point_on_networkline
    else:
        logger.debug("query is none check tolerance value of 200")
        return False


# use the rest_framework decorator to create our api
#  view for get, post requests
@api_view(['GET', 'POST'])
def create_route_from_coords(request, start_coord, start_floor, end_coord, end_floor, route_type):
    """
    Generate a GeoJSON indoor route passing in a start x,y,floor
    followed by &  then the end x,y,floor
    Sample request: http:/localhost:8000/api/v1/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2&0
    :param request:
    :param start_coord: start location x,y
    :param start_floor: floor number  ex)  2
    :param end_coord: end location x,y
    :param end_floor: end floor ex)  2
    :param route_type: type of route 1 = barrier-free ex) 1
    :return: GeoJSON route
    """

    if request.method == 'GET' or request.method == 'POST':

        # parse the incoming coordinates and floor using
        # split by comma
        x_start_coord = float(start_coord.split(',')[0])
        y_start_coord = float(start_coord.split(',')[1])
        start_floor_num = int(start_floor)

        x_end_coord = float(end_coord.split(',')[0])
        y_end_coord = float(end_coord.split(',')[1])
        end_floor_num = int(end_floor)

        # use our helper function to get vertices
        # node id for start and end nodes
        start_node_id = find_closest_network_node(x_start_coord,
                                                  y_start_coord,
                                                  start_floor_num)

        end_node_id = find_closest_network_node(x_end_coord,
                                                y_end_coord,
                                                end_floor_num)

        geojs_fc = run_route(start_node_id, end_node_id, route_type)

        try:
            return Response(geojs_fc)
        except:
            logger.error("error exporting to json model: " + str(geojs_fc))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')


def format_walk_time(walk_time):
    """
    takes argument: float walkTime in seconds
    returns argument: string time  "xx minutes xx seconds"
    """
    if walk_time > 0.0:
        return str(int(walk_time / 60.0)) + " minutes " + str(int(round(walk_time % 60))) + " seconds"
    else:
        return "Walk time is less than zero! something is wrong"


def calc_distance_walktime(rows):
    """
    calculates distance and walk_time.
    rows must be an array of linestrings --> a route, retrieved from the DB.
    rows[5]: type of line (stairs, elevator, etc)
    rows[3]: cost as length of segment
    returns a dict with key/value pairs route_length, walk_time
    """

    route_length = 0
    walk_time = 0

    for row in rows:

        route_length += row[3]
        # calculate walk time
        if row[5] == 3 or row[5] == 4:  # stairs
            walk_speed = 1.2  # meters per second m/s
        elif row[5] == 5 or row[5] == 6:  # elevator
            walk_speed = 1.1  # m/s
        else:
            walk_speed = 1.39  # m/s

        walk_time += (row[3] / walk_speed)

    length_format = "%.2f" % route_length
    real_time = format_walk_time(walk_time)
    return {"route_length": length_format, "walk_time": real_time}


def merge_2_routes(route_part1, route_part2):
    """
    Merges two route feature geometries into a single GeoJSON
    features list.
    :param route_part1 a valid route GeoJSON route result from A to B
    :param route_part2 a valid GeoJSON route result from B to C
    :return: the GeoJSON features key with all route segements
        of both routes from A to B and B to C where A is start
        B is middle destination and C is final destination
    """

    if route_part1:
        geo_features_route_part_1 = route_part1['features']  # list of geom
        geo_features_route_part_2 = route_part2['features']  # list of geom

        routes_merged = []

        routes_merged.extend(geo_features_route_part_1)
        routes_merged.extend(geo_features_route_part_2)

        return routes_merged
    else:
        return None


@api_view(['GET', 'POST'])
def force_route_mid_point(request, **kwargs):
    """
    Force a route over a middle point such as a front office
    :return: a single GeoJSON featureCollection with a middle point
    :param
    """
    start_node = request.GET.get('startnode', 1)  # 1385
    mnode = request.GET.get('midnode', 1)  # 1167
    end_node = request.GET.get('endnode', 1)  # 1252

    # building_id = 1
    route_nodes = {'building-id': 1, 'start-node-id': start_node, 'mid-node-id': mnode, 'end-node-id': end_node}

    # remove last coordinate of first route
    start_node_id = get_room_centroid_node(route_nodes['start-node-id'])
    mid_node_id = get_room_centroid_node(route_nodes['mid-node-id'])
    end_node_id = get_room_centroid_node(route_nodes['end-node-id'])

    route_start_to_mid_point = run_route(start_node_id, mid_node_id, 1)
    route_mid_to_end_point = run_route(mid_node_id, end_node_id, 1)

    route_out_merge = merge_2_routes(route_start_to_mid_point, route_mid_to_end_point)

    return Response({'type': 'FeatureCollection', 'features': route_out_merge})


@api_view(['GET',])
def route_to_nearest_poi(request, start_xy, floor, poi_cat_id):

    coords = start_xy.split("=")[1]
    x_start_coord = float(coords.split(',')[0])
    y_start_coord = float(coords.split(',')[1])
    start_floor_num = int(floor.split('=')[1])
    poi_cat_id_v = int(poi_cat_id.split("=")[1])

    startid = find_closest_network_node(x_start_coord, y_start_coord, start_floor_num)

    cur = connection.cursor()

    # bus = pk 27  underground= 26
    qs_nearest_poi = Poi.objects.filter(fk_poi_category=poi_cat_id_v)

    if qs_nearest_poi:
        dest_nodes = []
        pois_found = []

        for i, res in enumerate(qs_nearest_poi):
            network_node_id = find_closest_network_node(res.geom.coords[0][0], res.geom.coords[0][1], res.floor_num )
            if network_node_id:
                pois_found.append({"result_index": i, 'name': res.name, 'floor': res.floor_num, 'id': res.id,
                                 'network_node_id': network_node_id, 'geometry':loads(res.geom.geojson)})

                dest_nodes.append(network_node_id)
            else:
                return Response({"error": "no network node found close to poi"}, status=status.HTTP_400_BAD_REQUEST)



        pgr_query = """SELECT end_vid, sum(cost) as distance_to_poi
            FROM pgr_dijkstra(
                'SELECT id, source, target, cost FROM geodata.networklines_3857',
                {start_node_id}, ARRAY{poi_ids},FALSE
                -- 2, ARRAY[1077, 1255],
                 )
            GROUP BY end_vid
            ORDER BY distance_to_poi asc
            LIMIT 1;""".format(start_node_id=startid, poi_ids=dest_nodes)


        cur.execute(pgr_query)
        res = cur.fetchall()

        node_id_closest_poi = res[0][0]

        closest_poi = None

        for x in pois_found:
            if node_id_closest_poi == x['network_node_id']:
                closest_poi = x


        geojs_fc = run_route(startid, node_id_closest_poi, 1)
        geojs_fc.update({'route_info':[{'destination':closest_poi},{'start': 'work in progress'}]})

        return Response(geojs_fc)
    else:
        return Response({"error":"no Pois with that poi_cat_id found"}, status=status.HTTP_400_BAD_REQUEST)


def set_route_start_end_feature():
    # add the name of the start route item and destination route item
    pass


def run_route(start_node_id, end_node_id, route_type):
    """

    :param start_node_id:
    :param end_node_id:
    :param route_type:
    :param route_options: a dictionary
    :return:
    """
    # TODO add route options dictionary
    # TODO add parameter to function   route_options=None

    # sample dictionary of options
    # route_options = {'route_types': {
    #     'standard_route': 1,
    #     'barrierfree route': 2,
    #     'indoor_only_prefered': 3,
    #     'fastest': 4
    # },
    #     'route_logic': {
    #         'force_route_through_location': True
    #     }
    # }

    cur = connection.cursor()
    # base_route_q = """SELECT id, source, target,
    #                  total_cost:: DOUBLE PRECISION AS cost,
    #                  floor, network_type
    #                  FROM geodata.networklines_3857"""
    base_route_q = """SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857"""

    # set default query
    barrierfree_q = "WHERE 1=1"
    if route_type == "1":
        # exclude all networklines of type stairs
        barrierfree_q = "WHERE network_type not in (1,3)"


    # routing_query = '''
    #  SELECT seq, id, node, edge, ST_Length(geom) AS cost, floor, network_type, ST_AsGeoJSON(geom) AS geoj
    #   FROM pgr_dijkstra( '{normal} {type}', %s, %s, FALSE) AS dij_route
    #   LEFT JOIN geodata.networklines_3857 AS input_network
    #   ON dij_route.edge = input_network.id
    #   ORDER BY dij_route.seq;
    # '''.format(normal=base_route_q,type=barrierfree_q)
    route_query = "SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857"

    routing_query = """
        SELECT seq, id, node, edge,
            ST_Length(geom) AS cost, agg_cost, floor, network_type,
            ST_AsGeoJSON(geom) AS geoj
        FROM pgr_dijkstra( '{normal} {type}',{start_node}, {end_node}) AS dij_route

          JOIN geodata.networklines_3857 AS input_network
          ON dij_route.edge = input_network.id ;""".format(normal=route_query, type=barrierfree_q, start_node=start_node_id, end_node=end_node_id)


    # routing_query = '''
    #     SELECT seq,
    #     id1 AS node,
    #     id2 AS edge,
    #       ST_Length(geom) AS cost,
    #        floor,
    #       network_type,
    #       ST_AsGeoJSON(geom) AS geoj
    #       FROM pgr_dijkstra('
    #         {normal} {type}', %s, %s, FALSE, FALSE
    #       ) AS dij_route
    #       JOIN  geodata.networklines_3857 AS input_network
    #       ON dij_route.id2 = input_network.id ;
    #   '''.format(normal=base_route_q, type=barrierfree_q)

    # run our shortest path query
    if start_node_id or end_node_id:
        if start_node_id != end_node_id:
            # cur.execute(routing_query, (start_node_id, end_node_id))
            cur.execute(routing_query)
    else:
        logger.error("start or end node is None or is the same node " + str(start_node_id))
        return HttpResponseNotFound('<h1>Sorry NO start or end node'
                                    ' found within 200m</h1>')

    # get entire query results to work with
    route_segments = cur.fetchall()

    route_info = calc_distance_walktime(route_segments)

    # empty list to hold each segment for our GeoJSON output
    route_result = []

    # loop over each segment in the result route segments
    # create the list of our new GeoJSON
    for segment in route_segments:
        seg_length = segment[4]  # length of segment
        layer_level = segment[6]  # floor number
        seg_type = segment[7]
        seg_node_id = segment[2]
        seq_sequence = segment[0]
        geojs = segment[8]  # geojson coordinates
        geojs_geom = loads(geojs)  # load string to geom
        geojs_feat = Feature(geometry=geojs_geom,
                             properties={'floor': layer_level,
                                         'segment_length': seg_length,
                                         'network_type': seg_type,
                                         'seg_node_id': seg_node_id,
                                         'sequence': seq_sequence}
                             )
        route_result.append(geojs_feat)

    # using the geojson module to create our GeoJSON Feature Collection
    geojs_fc = FeatureCollection(route_result)
    geojs_fc.update(route_info)
    return geojs_fc


@api_view(['GET', 'POST'])
def create_route_from_id(request, start_room_id, end_room_id, route_type):
    """
    Generate a GeoJSON route from external room id
    to external room id
    :param building_id: id of building as integer
    :param request: GET or POST request
    :param start_room_id: an integer room number
    :param end_room_id: an integer room number
    :param route_type: an integer room type
    :return: a GeoJSON linestring of the route
    """

    if request.method == 'GET' or request.method == 'POST':

        start_room = int(start_room_id.split("=")[1])
        end_room = int(end_room_id.split("=")[1])
        # building_id = int(building_id.split("=")[1])

        start_node_id = get_room_centroid_node( start_room)
        end_node_id = get_room_centroid_node( end_room)

        res = run_route(start_node_id, end_node_id, route_type)

        try:
            return Response(res)
        except:
            logger.error("error exporting to json model: " + str(res))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')


def get_features(FeatureCollection):
    props_list = []
    for feature in FeatureCollection:
        props_list.append(feature['properties'])

    return props_list

@api_view(['GET', 'POST'])
def create_route_from_search(request, start_term, end_term, route_type=0):
    """
    Generate a GeoJSON route from room number
    to room number
    :param request: GET or POST request
    :param building_id: buiilding id as integer
    :param start_term: a text string as search term
    :param end_term: a text string as search term
    :param route_type: an integer room type
    :return: a GeoJSON linestring of the route
    """

    if request.method == 'GET' or request.method == 'POST':



        start_room = start_term.split("=")[1]
        end_room = end_term.split("=")[1]

        res_start_searchany = requests.get(url=settings.LOCALHOST_URL + "search/{0}".format(start_room), verify=False)
        fx1 = res_start_searchany.json()

        start_aks = fx1['features'][0]['properties']['aks_nummer']

        res_end_searchany = requests.get(url=settings.LOCALHOST_URL + "search/{0}".format(end_room), verify=False)
        fx2 = res_end_searchany.json()

        end_aks = fx2['features'][0]['properties']['aks_nummer']

        if start_aks:
            start_room = start_aks

        if end_aks:
            end_room = end_aks




        cur = connection.cursor()
        # logger.debug('*************************start term' + str(start_room))
        # logger.debug('*************************end term' + str(end_room))

        start_query = """SELECT id, external_id, search_string FROM geodata.search_index_v
                          WHERE search_string LIKE '%{0}%'
                          OR external_id = '{0}'
                          ORDER BY length(search_string) LIMIT 1""".format(start_room)

        # logger.debug('**************print query' + str(start_query))
        cur.execute(start_query)

        get_start_id_list = cur.fetchone()
        start_id_value = get_start_id_list[0]

        end_query = """SELECT id, external_id, search_string FROM geodata.search_index_v
                          WHERE search_string LIKE '%{0}%'
                          OR external_id = '{0}'
                          ORDER BY length(search_string) LIMIT 1""".format(end_room)

        # logger.debug('**************print END  query' + str(end_query))
        cur.execute(end_query)

        get_end_id_list = cur.fetchone()
        end_id_value = get_end_id_list[0]

        # logger.debug('*************************current start id' + str(start_id_value))
        # logger.debug('*************************current end id' + str(end_id_value))

        start_node_id = get_room_centroid_node( start_id_value )
        end_node_id = get_room_centroid_node( end_id_value )

        res = run_route(start_node_id, end_node_id, route_type)

        try:
            return Response(res)
        except:
            logger.error("error exporting to json model: " + str(res))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')


@api_view(['GET', 'POST'])
def create_route_from_search2(request, start_term, end_term, route_type=0):
    """
    Generate a GeoJSON route from room number
    to room number
    :param request: GET or POST request
    :param building_id: buiilding id as integer
    :param start_term: a text string as search term
    :param end_term: a text string as search term
    :param route_type: an integer room type
    :return: a GeoJSON linestring of the route
    """

    if request.method == 'GET' or request.method == 'POST':

        start_aks = start_term.split("=")[1]
        end_aks = end_term.split("=")[1]

        if start_aks:
            start_room = start_aks

        if end_aks:
            end_room = end_aks

        start_node_id = find_closest_network_node(x_start_coord, y_start_coord, start_floor)
        end_node_id = find_closest_network_node(x_end_coord, y__end_coord, end_floor)


        res = run_route(start_node_id, end_node_id, route_type)

        try:
            return Response(res)
        except:
            logger.error("error exporting to json model: " + str(res))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')