# Create your views here.
# coding: utf-8
# !/opt/.venvs/wuwien/bin python

import json
from rest_framework.decorators import api_view


from django.http import  HttpResponse

import logging

logr = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# takes a dict with searchcriteria, and returns the POI list.
# param: searchcriteria, containing data for searching. "type" attribute is mandatory!
# returns: a list with all pois (poi is represented as dict with lat, lon, layer,...)
# returns the entrance which is nearest to this room+

def create_terminal_start_json(query_result):
    '''

    :param query_result: psycopg2 response tuple or None
    :return: JSON of entrance for terminal start location
    '''
    returnList = []
    entranceCoords = json.loads(query_result[0])
    coords = entranceCoords['coordinates']
    entranceLayer = query_result[3]
    entranceEntry = {"lat": coords[1], "lon": coords[0], "layer": entranceLayer,
                     "routeNodeAttributes": {"name_de": query_result[2], "name_en": query_result[2],
                                             "layer": entranceLayer}, "terminalIp": query_result[4], }
    returnList.append(entranceEntry)
    terminal_start_json = json.dumps(returnList[0])
    return terminal_start_json


@api_view(['GET', ])
def getPoiTerminalData(request):
    """
    return a LIST of all POIs either with "entrance" or "ubahn" in the column "name"
    """
    ipTerminal = get_client_ip(request)
    if ipTerminal == "127.0.0.1":
        ipTerminal = "143.205.84.105"

    from django.db import connection
    cur = connection.cursor()

    # note aks_nummer column stores Terminal IP value in POI_LIST tabel
    query_get_ter = "select st_asgeojson(st_pointonsurface(geom)), description, description_en, floor, aks_nummer " \
                    "from geodata.poi_list where aks_nummer LIKE '{0}'".format(ipTerminal)

    cur.execute(query_get_ter)
    entrance = cur.fetchone()

    # bring in format: [{lat: .. lon: ... routeNodeAttributes:{"name": ..., "name_de": ...}},....]
    if entrance:
        terminal_start = create_terminal_start_json(entrance)

        return HttpResponse(terminal_start, content_type="application/json")
    else:
        # note aks_nummer column stores Terminal IP value in POI_LIST tabel
        query_non_terminal_req = "SELECT st_asgeojson(st_pointonsurface(geom)), description, description_en, floor, aks_nummer " \
                                 "FROM geodata.poi_list WHERE description = 'LC Eingang'"

        cur.execute(query_non_terminal_req)
        non_terminal_start_resp = cur.fetchone()
        terminal_start = create_terminal_start_json(non_terminal_start_resp)

        return HttpResponse(terminal_start, content_type="application/json")


#@jsonrpc_method('routeFromTerminal(q=dict) -> dict')

@api_view(['GET', ])
def route_from_terminal(request, q):
    if q is None:
        return json.dumps({'myerror': 'q param is None !  why we dont know not good'})
    else:

        searchType = q["searchCriteria"]["type"]
        if searchType == "terminal":
            # if searchType:
            from django.db import connection
            cur = connection.cursor()

            # terminal_ip = get_client_ip(request)
            terminal_data = getPoiTerminalData(request)

            if terminal_data:
                terminal_dict = json.loads(terminal_data.content)

                lon = q["lon"]
                lat = q["lat"]
                layer = q["layer"]

                terminal_start = {"lat": terminal_dict["lat"], "lon": terminal_dict["lon"],
                                  "layer": terminal_dict["layer"],
                                  "routeNodeAttributes": {"name_de": terminal_dict["routeNodeAttributes"]["name_de"],
                                                          "name_en": terminal_dict["routeNodeAttributes"]["name_en"],
                                                          "layer": "0"}}

                nodes = [{"lat": lat, "lon": lon, "layer": layer, "routeNodeAttributes": q["routeNodeAttributes"]},
                         terminal_start]
                qDict = {"disabled": False, "nodes": nodes}
                # get frontoffice if needed

                # logr.debug("your ip is : " + str(terminal_ip))
                # logr.debug("your termain data is : " + str(terminal_data))
                # logr.debug("your termain diction is : " + str(terminal_dict))

                #qDict2 = json.loads(getForcedMiddlePointIfExists(cur, qDict))

                #return json.dumps(qDict2)
                return json.dumps(qDict)
            else:
                return json.dumps({'error': ' no terminal found do normal route'})
        else:
            return json.dumps(
                {'error': ' search type NOT "terminal"  in string something went wacky hmm in route_from_terminal'})


@api_view(['GET'])
def route_from_kiosk(request, rvk_id):
    """
    Create a route directly to a book based on RVK key
    :param request:
    :param rvk_id: rvk_id
    :return: GeoJson linestring route from building entrance to book
    """

    fix_start_location = "1826545.2173675,6142423.4241214,0&"

    book_location_resp = rvk_call(request, rvk_id)

    resp = json.loads(str(book_location_resp.data))

    if resp['features'][1]['geometry']['type'] == 'Point':
        dest_floor = resp['features'][1]['properties']['floor']
        dest_coord_x = resp['features'][1]['geometry']['coordinates'][0]
        dest_coord_y = resp['features'][1]['geometry']['coordinates'][1]

        dest_coords = str(dest_coord_x) + "," + str(dest_coord_y)

        # print('/api/v1/directions/'+ fix_start_location + dest_coord + "," + dest_floor + "&0" )
        url = 'http://localhost:8000/api/v1/directions/' + fix_start_location + dest_coords + ',' + dest_floor + '&0'
        route_to_book = requests.get(url)

        return Response(route_to_book.json())
