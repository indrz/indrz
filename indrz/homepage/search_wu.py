# search anything on campus
import json
import pprint
import ast

from django.http import HttpResponse
import logging
from homepage import bach_calls

# from django.http import Http404, HttpResponse, HttpResponseServerError
# from django.db.utils import DatabaseError
# from django.core.exceptions import PermissionDenied
# from models import Language
# import re
# from log_routes import log_request
from rest_framework.decorators import api_view
from rest_framework.response import Response

from geojson import Feature, FeatureCollection

logr = logging.getLogger(__name__)


# search for what is close to a given coordinate and return a list
# of strings and coordinates - coordinates must contain Lon, Lat and Layer

# @jsonrpc_method('searchCoordinates(q=dict) -> dict', validate=True)
@api_view(['GET'])
def search_coordinates(request, q):
    if q.keys().index('coordinates') < 0:
        raise Exception("Couldn't find coordinates in Parameter q")
    coordinates = q['coordinates']
    lon = float(coordinates['lon'])
    lat = float(coordinates['lat'])
    layer = int(coordinates['layer'])

    distance_bound = 5  # 5 meters

    # build geom string - this should be safe from any sql injection as lon and lat are both floats
    geom = "ST_SetSrid(ST_GeomFromText('POINT(" + str(lon) + " " + str(lat) + ")'),900913)"

    sql = "SELECT search_string, text_type, external_id, st_asgeojson(geom) as geom, \
        st_asgeojson(st_PointOnSurface(geom)) as center, \
        ST_Distance( geom," + geom + ") as dist, layer, external_ref_name, aks_nummer, building \
        FROM geodata.search_index_v \
        WHERE layer=%(layer)s \
            AND ST_Distance( geom," + geom + " ) < %(distance_bound)s \
        ORDER BY priority DESC, ST_Distance(geom," + geom + ") ASC LIMIT 9"

    rows = []

    from django.db import connection

    cursor = connection.cursor()

    cursor.execute(sql,
                   {"layer": layer, "distance_bound": distance_bound})
    db_rows = cursor.fetchall()

    for row in db_rows:
        external_ref_name = row[7]
        # query to bach api
        external_data = bach_calls.bach_get_room_by_pk_big(external_ref_name)

        name_de = name_en = row[0]
        if external_data is not None and 'roomcode' in external_data:  # old value was 'roomname' now roomcode
            name_de = name_en = external_data['roomcode']
            # end if

        obj = {"name_de": name_de, "name_en": name_en, "type": row[1], "external_id": row[2], "geometry": row[3],
               "centerGeometry": row[4], "dist": row[5], "layer": int(row[6]), "aks_nummer": row[8], "building": row[9],
               "externalRefName": external_ref_name,
               "externalData": external_data,
               }
        new_feature = Feature(geometry=row[3], properties=obj)
        rows.append(new_feature)

    searchString = str(lon) + "," + str(lat) + "," + str(layer)

    retVal = {"searchString": searchString, "searchResult": rows, "length": len(db_rows)}

    return Response(retVal)


# search for what is close to a given coordinate and return a list of strings and coordinates
# - coordinates must contain Lon, Lat and Layer
# @jsonrpc_method('searchCoordinatesPOI(q=dict) -> dict', validate=True)

@api_view(['GET'])
def search_coordinates_on_poi(request, q):
    if q.keys().index('coordinates') < 0:
        raise Exception("Couldn't find coordinates in Parameter q")
    coordinates = q['coordinates']
    lon = float(coordinates['lon'])
    lat = float(coordinates['lat'])
    layer = int(coordinates['layer'])

    distance_bound = 1  # 5 meters

    # build geom string - this should be safe from any sql injection as lon and lat are both floats
    geom = "ST_SetSrid(ST_GeomFromText('POINT(" + str(lon) + " " + str(lat) + ")'),900913)"

    sql = "SELECT search_string, text_type, external_id, ST_asgeojson(geom) as geom, \
    ST_asgeojson(ST_PointOnSurface(geom)) as center, \
    ST_Distance(geom," + geom + ") as dist, layer, external_ref_name, aks_nummer, building \
    FROM geodata.search_index_v \
    WHERE text_type='poi' \
    AND layer=%(layer)s \
    AND ST_Distance(geom," + geom + ") < %(distance_bound)s \
    ORDER BY priority DESC, ST_Distance(geom," + geom + ") \
    ASC LIMIT 9"

    rows = []

    from django.db import connection

    cursor = connection.cursor()
    cursor.execute(sql,
                   {"layer": layer, "distance_bound": distance_bound})
    dbRows = cursor.fetchall()
    for row in dbRows:
        external_ref_name = row[7]
        # query to bach api
        external_data = bach_calls.bach_get_room_by_pk_big(external_ref_name)
        obj = {"name_de": row[0], "name_en": row[0], "type": row[1], "external_id": row[2], "geometry": row[3],
               "centerGeometry": row[4], "dist": row[5], "layer": int(row[6]), "aks_nummer": row[8], "building": row[9],
               "externalRefName": external_ref_name,
               "externalData": external_data,
               }
        rows.append(obj)

    searchString = str(lon) + "," + str(lat) + "," + str(layer)

    retVal = {"searchString": searchString, "searchResult": rows, "length": len(dbRows)}

    return Response(retVal)


def repNoneWithEmpty(string):
    if string is None:
        return ''
    else:
        return str(string)


# returns the entrance which is nearest to this room+
@api_view(['GET'])
def getAssignedEntrance(request, aks, layer):
    """
    input aks as string
    input layer as integer

    output dictionary of entrance-id,
         entrance-name-de, entrance-name-en,
         entrance-lat, entrance-lon
    """
    from django.db import connection

    cursor = connection.cursor()

    sql = "SELECT entrance_poi_id FROM geodata."

    if (layer == -1 or layer == "-1"):
        sql += "ug01"
    elif (layer == 0 or layer == "0"):
        sql += "eg00"
    elif (layer > 0):
        sql += "og0" + str(layer)

    sql += "_rooms where aks_nummer = %(aks)s"
    cursor.execute(sql, {"aks": aks})
    results = cursor.fetchall()

    if len(results) > 0:
        entranceID = results[0][0]

        cursor.execute(
            "SELECT description, description_en, ST_asgeojson(geom) AS geojson_geom FROM geodata.poi_list WHERE id=%(id)s",
            {"id": entranceID})
        res = cursor.fetchall()

        if cursor.rowcount > 0:
            entrance_point = json.loads(res[0][2])
            entrance_lat = entrance_point["coordinates"][1]
            entrance_lon = entrance_point["coordinates"][0]

        if len(res) > 0:
            valid_resp = {"id": repNoneWithEmpty(entranceID), "de": repNoneWithEmpty(res[0][0]),
                    "en": repNoneWithEmpty(res[0][1]),
                    "entrance_lat": entrance_lat,
                    "entrance_lon": entrance_lon}

            return Response(valid_resp)
    # if nothing found
    invalid_return = {"id": "", "de": "", "en": "", "entrance_lat": "", "entrance_lon": ""}
    return Response(invalid_return)


    # search for strings and return a list of strings and coordinates


def has_front_office(orgid):
    """

    :param data:
    :return:
    """

    from django.db import connection
    cursor = connection.cursor()

    if orgid != None and orgid != "":
        organization_details = bach_calls.bach_get_organization_details(orgid)
        if organization_details != None and len(organization_details) > 0:
            org_info = {"location": organization_details["location"],
                        "name": organization_details["label"],
                        "geom": None}

            query_geo = """SELECT  st_asgeojson(st_PointOnSurface(geom)) AS center
              FROM geodata.search_index_v
              WHERE external_id = \'{0}\'""".format(organization_details["location"])

            cursor.execute(query_geo)
            geos = cursor.fetchone()

            foo = ast.literal_eval(geos[0])

            org_info.update({'geom': foo})

            return org_info
    else:
        return None

# @jsonrpc_method('searchAny(q=dict) -> dict', validate=True)
@api_view(['GET'])
def search_any(request, q):
    # if q.keys().index('searchString') < 0:
    #     raise Exception("Couldn't find searchString in parameter q")
    # searchString = q['searchString']

    searchString = q

    # dont allow empty searchString, too short searchString or too long searchstring (50 characters is way too much
    #  and probably a sql attack so we prevent it here aswell
    if searchString == "" or len(searchString) < 2 or len(searchString) > 100:
        raise Exception("searchString is too short. Must be at least 2 characters")

    # check for possible sql attacks etc...
    if '}' in searchString or '{' in searchString or ';' in searchString:
        raise Exception("illegal characters in searchString")

    extraBuilding = ''

    # rows-array which will contain the return dataset


    from django.db import connection

    cursor = connection.cursor()


    # query bach api rooms for room data
    bachData = []
    room_data_results = bach_calls.bach_search_rooms(searchString)
    if room_data_results != None:
        bachData.extend(room_data_results)

    # print(bachData)

    # =============================================
    # extend d organisations and people data in one
    bachOrgs = bach_calls.bach_search_directory(searchString)
    bachData.extend(bachOrgs)
    # .pprint(bachData)
    # uncomment following for orgs without persons
    # if len(bachOrgs) > 0:
    #     for row in bachOrgs:
    #         if row.get("firstName") == None:
    #             bachData.append(row)
    # =============================================

    bachDataLength = 0
    bachLocationStrings = []
    bachLocationList = {}

    if bachData != None and len(bachData) > 0:
        bachDataLength = len(bachData)
        cnt = 0

        for row in bachData:
            # searchstring has to be in label, name_de or name_en (persons only have label, so check if name_de/name_en exists)
            if ("label" in row and searchString.upper() in row["label"].upper()) or \
                    ("roomcode" in row and searchString.upper() in row["roomcode"].upper()) or \
                    ("roomname_en" in row and searchString.upper() in row["roomname_en"].upper()) or \
                    ("roomname_de" in row and searchString.upper() in row["roomname_de"].upper()) or \
                    ("pk_big" in row and searchString.upper() in row["pk_big"].upper()) or \
                    ("name" in row and searchString.upper() in row["name"].upper()) or \
                    ("name_de" in row and searchString.upper() in row["name_de"].upper()) or \
                    ("name_en" in row and searchString.upper() in row["name_en"].upper()) or \
                    ("category_de" in row and searchString.upper() in row["category_de"].upper()) or \
                    ("category_en" in row and searchString.upper() in row["category_en"].upper()):

                # if location (aks) is not null, use it
                if 'location' in row and row['location'] is not None or \
                                        'pk_big' in row and row['pk_big'] is not None or \
                                                'currentAffiliation' in row and row[
                                    "currentAffiliation"] is not None and row["currentAffiliation"][0][
                            "orgid"] is not None:

                    locationDict = {"location": ""}

                    roomcode_value = None

                    cat_de_value = None
                    cat_en_value = None
                    roomcode_value = None
                    building_name = None

                    if 'buildingname' in row:
                        building_name = row['buildingname']

                    if 'category_en' in row and row['category_en'] is not None:
                        cat_en_value = row['category_en']
                    if 'category_de' in row and row['category_de'] is not None:
                        cat_de_value = row['category_de']

                    # empty dictionaries evaluate to False in pyton so we check for is False
                    if 'location_struc' in row and row['location_struc'] is not None:
                        location_values = row['location_struc']


                        # test if dict item is an empty dictionary if yes skip if not
                        if location_values:  # evaluates to TRUE meaning if NOT empty {}
                            if "roomname_de" in location_values:
                                roomcode_value = row["location_struc"]["roomname_de"]
                                building_name = row['location_struc']['buildingname']
                    else:
                        roomcode_value = ""


                    # distinguish between normal (aks = location), search by pk, and persons (location can be found in currentaffiliaton)
                    if 'location' in row and row['location'] is not None:
                        locationDict = {"location": row["location"]}
                    elif 'pk_big' in row and row['pk_big'] is not None:
                        locationDict = {"location": row["pk_big"]}
                    elif 'currentAffiliation' in row and row["currentAffiliation"] is not None and \
                                    row["currentAffiliation"][0]["orgid"] is not None:
                        organization_details = bach_calls.bach_get_organization_details(
                            row["currentAffiliation"][0]["orgid"])
                        if organization_details != None and len(organization_details) > 0:
                            locationDict = {"location": organization_details["location"]}

                    cursor.execute("SELECT search_string, text_type, external_id, st_asgeojson(geom) AS geom, \
                     st_asgeojson(st_PointOnSurface(geom)) AS center,\
                     layer, building_id, 0 AS resultType, external_id, text_type, room_code, id AS space_id \
                     FROM geodata.search_index_v \
                     WHERE external_id = upper(%(location)s)", locationDict)

                    result = cursor.fetchall()

                    if len(result) > 0:
                        # getting orgid. rooms have an attribute, persons have ["currentAffiliation"][0]["orgid"]
                        orgid = ""
                        if "orgid" in row and row["orgid"] is not None:
                            orgid = row["orgid"]
                        elif "currentAffiliation" in row and row["currentAffiliation"][0]["orgid"] is not None:
                            orgid = row["currentAffiliation"][0]["orgid"]

                        # if name_de/en is present in search people, use it,
                        # else use label,
                        # else result is a room from room search and name is roomname_de/en use that
                        if ("name" in row ):
                            name = row["name"]

                        else:
                            name = ""


                        if "name_de" in row:
                            name_de = row["name_de"]
                            name = name_de
                        else:
                            name_de =""


                        if ("label" in row):
                            label = row["label"]
                        else:
                            label = ""


                        # no name data means we only have room data
                        if ("roomname_en" in row and "roomname_de" in row):
                            roomname_en = row["roomname_en"]
                            roomname_de = row["roomname_de"]
                        else:
                            roomname_en = ""
                            roomname_de = ""

                        if ("fancyname_de" in row and "fancyname_en" in row):
                            fancyname_en = row['fancyname_en']
                            fancyname_de = row['fancyname_de']
                        else:
                            fancyname_en = None
                            fancyname_de = None

                        if 'roomcode' in row:
                            roomcode = row['roomcode']
                        else:
                            roomcode = ""

                        if 'category_de' in row:
                            cat_de_value = row['category_de']
                        else:
                            cat_de_value = ""

                        if 'category_en' in row:
                            cat_en_value = row['category_en']
                        else:
                            cat_en_value = ""



                        # if cat_de_value is not None:
                        #     cat_de_encode = cat_de_value.encode('utf-8')
                        #     cat_en_encode = cat_en_value.encode('utf-8')
                        # else:
                        #     cat_de_encode = ""
                        #     cat_en_encode = ""
                        # ==========================================================
                        # find out location of frontoffice
                        roomcode_value = repNoneWithEmpty(result[0][10])

                        if roomcode_value == '':
                            roomcode_value = None


                        # front_office = ""
                        front_office = has_front_office(orgid)
                        # if orgid != None and orgid != "":
                        #     organization_details = bach_calls.bach_get_organization_details(orgid)
                        #     if organization_details != None and len(organization_details) > 0:
                        #         frontoffice = organization_details["location"]
                        if name == "":
                            if roomcode_value is not "":
                                name = roomcode_value



                        obj = {"name": repNoneWithEmpty(name),
                               "label" : repNoneWithEmpty(label),
                               "room_name_en": repNoneWithEmpty(roomname_en),
                               "room_name_de": repNoneWithEmpty(roomname_de),
                               "fancyname_de": repNoneWithEmpty(fancyname_de),
                               "fancyname_en": repNoneWithEmpty(fancyname_en),
                               "roomcode": roomcode_value,
                               "type": repNoneWithEmpty(result[0][1]),
                               "external_id": repNoneWithEmpty(result[0][2]),
                               # "geometry": ast.literal_eval(result[0][3]),
                               "centerGeometry": ast.literal_eval(result[0][4]),
                               "floor_num": repNoneWithEmpty(int(result[0][5])),
                               "building": repNoneWithEmpty(result[0][6]),
                               "building_name": building_name,
                               "aks_nummer": repNoneWithEmpty(locationDict["location"]),
                               "orgid": repNoneWithEmpty(orgid),
                               "frontoffice": front_office,
                               "category_de": repNoneWithEmpty(cat_de_value),
                               "category_en": repNoneWithEmpty(cat_de_value),
                               "space_id": repNoneWithEmpty(result[0][11]),
                               "src": "bach"
                               }

                        new_feature_geojson = Feature(geometry=ast.literal_eval(result[0][3]), properties=obj)

                        bachLocationStrings.append(new_feature_geojson)

                else:
                    pass

    if len(bachLocationStrings) > 0:
        # --------------------------------------------------------
        # add the assigned entrance
        for tempResult in bachLocationStrings:
            if (tempResult["properties"]["aks_nummer"] is not None and tempResult["properties"][
                "aks_nummer"] != ""):
                # entranceData = getAssignedEntrance(tempResult["aks_nummer"], tempResult["layer"]);
                # tempResult["entrance"] = entranceData["id"];
                # tempResult["entrance_name_de"] = entranceData["de"];
                # tempResult["entrance_name_en"] = entranceData["en"];
                pass

        # --------------------------------------------------------
        retVal = {"searchString": searchString, "building": '', "searchResult": bachLocationStrings,
                  "length": bachDataLength}

        final_geojs_res = FeatureCollection(features=bachLocationStrings)
        return Response(final_geojs_res)

    # =================================================================================================================================
    # bach data finished, if entries present --> return them, else do a lookup in our local data.
    else:
        # do local search in DB no BACH API results found

        # query table or view: rooms
        # query columns: room_name
        # Order by similarity? LIMIT to 10
        # need to return: room_name, room_number, coordinates

        # add % at the beginning and end of the search string so we can use it in the like statement
        # also convert searchString toUpper here
        searchString2 = "%" + searchString.upper() + "%"
        extraBuilding2 = "%" + extraBuilding.upper() + "%"

        local_db_results = []

        sql = """
        SELECT search_string, text_type, external_id, st_asgeojson(geom) AS geom,
            st_asgeojson(st_PointOnSurface(geom)) AS center, layer, building_id, 0 AS resultType,
            external_id, room_code, id
                FROM geodata.search_index_v
                WHERE upper(search_string) LIKE %(search_string)s
                ORDER BY search_string DESC, length(search_string) LIMIT 9
        """

        cursor.execute(sql,
                       {"search_string": searchString2, "building": extraBuilding2,
                        "bach_location_list": tuple(bachLocationStrings)})
        db_rows = cursor.fetchall()

        for row in db_rows:
            loc = row[8]  # row[8] is AKS_NUMMER
            roomcode_value = row[9]  # roomcode

            if roomcode_value == '':
                roomcode_value = None


            poi_id = row[1]
            if poi_id == 'poi':
                poi_id = repNoneWithEmpty(int(row[10]))

                # our search string
            obj = {"label": row[0], "name": row[0], "type": row[1], "external_id": row[2],
                   "centerGeometry": ast.literal_eval(row[4]), "floor_num": repNoneWithEmpty(int(row[5])),
                   "building": repNoneWithEmpty(row[6]), "aks_nummer": loc, "roomcode_value": repNoneWithEmpty(roomcode_value),
                   "src": "local db view", "poi_id" : poi_id
                   # , "frontoffice": "001_10_OG04_421600", "orgid": "1234"
                   }


            poi_feature_geojson = Feature(geometry=ast.literal_eval(row[3]), properties=obj)
            local_db_results.append(poi_feature_geojson)


        # --------------------------------------------------------
        # add the assigned entrance
        # for tempResult in rows:
        #     if (tempResult["aks_nummer"] is not None and tempResult["aks_nummer"] != ""):
        #         #entranceData = getAssignedEntrance(tempResult["aks_nummer"], tempResult["layer"]);
        #         #tempResult["entrance"] = entranceData["id"];
        #        # tempResult["entrance_name_de"] = entranceData["de"];
        #         #tempResult["entrance_name_en"] = entranceData["en"];
        #         pass
        # --------------------------------------------------------
        # retVal = {"searchString": searchString, "building": extraBuilding, "searchResult": local_db_results, "length": len(db_rows)}

        local_data_geojson = FeatureCollection(features=local_db_results)

        return Response(local_data_geojson)

@api_view(['GET'])
def searchAutoComplete(request, search_text):
    # searchString = request.GET["query"]
    searchString = search_text
    if (searchString != None):

        items = []

        # ===========================================================================
        # bach data

        # ======================================================
        # append organizations but no persons!
        bachData = bach_calls.bach_search_directory(searchString)
        if bachData is not None:
            for row in bachData:
                if "label" in row and searchString.upper() in row["label"].upper():

                    name = ""
                    if ("label" in row and searchString == row["label"]):
                        name = row["label"]
                    elif ("name_de" in row and searchString == row["name_de"]):
                        name = row["name_de"]
                    elif ("name_en" in row and searchString == row["name_en"]):
                        name = row["name_en"]
                    else:
                        name = row["label"]

                    # remove whitespaces at the end of string (for duplicate detection)
                    name = name.strip()
                    # items.append({"name": name})
                    items.append(name)

        # ======================================================

        bachData_rooms = bach_calls.bach_search_rooms(searchString)

        room_cat = None

        if bachData_rooms is not None:
            for row in bachData_rooms:
                # searchString = unicode(searchString, "utf-8") # convert our string to unicode
                if "category_de" in row and searchString.upper() in row["category_de"].upper():

                    room_cat = ""
                    x = row['category_de']
                    room_cat = row["category_de"]

                    # remove whitespaces at the end of string (for duplicate detection)
                    room_cat = room_cat.strip()
                    # items.append({"name": room_cat})
                    items.append(room_cat)

                elif "category_en" in row and searchString.upper() in row["category_en"].upper():
                    room_cat = row['category_en']
                    room_cat = room_cat.strip()
                    # items.append({"name": room_cat})
                    items.append(room_cat)

        # ===========================================================================
        # local Postgresql search_index_v data

        from django.db import connection

        cursor = connection.cursor()

        searchString = searchString.replace(".", "", 2)
        searchString = searchString.replace(" ", "", 2)

        cursor.execute("""SELECT search_string FROM geodata.search_index_v
                          WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper(%(search_string)s)
                          GROUP BY search_string
                          LIMIT 100""",
                       {"search_string": "%" + searchString + "%"})

        rows = cursor.fetchall()
        # return HttpResponse(cursor.query)

        for row in rows:
            # item = {'name': row[0].strip()}
            item = row[0].strip()
            items.append(item)
        # ===========================================================================
        # END local data

        # remove duplicate entries

        output = []
        for x in items:
            if x not in output:
                output.append(x)
        # return HttpResponse(request.GET["callback"] + "(" + json.dumps({'result': output}) + ")")
        # return HttpResponse(json.dumps({'result':items}))
        return Response(output)


# @api_view(['GET'])
# def wuAutoComplete(request, search_text):
#     """
#     Example:
#     /autocomplete/Erste
#
#     :param request:
#     :return:
#     """
#     # searchString = request.GET["query"]
#     searchString = search_text
#     if (searchString != None):
#
#         items = []
#
#
#         # ===========================================================================
#         # bach data
#
#         #======================================================
#         #append organizations but no persons!
#         bachData = bach_calls.bach_search_directory(searchString)
#         if bachData is not None:
#             for row in bachData:
#                 if "label" in row and searchString.upper() in row["label"].upper():
#
#                     name = ""
#                     if ("label" in row and searchString == row["label"]):
#                         name = row["label"]
#                     elif ("name_de" in row and searchString == row["name_de"]):
#                         name = row["name_de"]
#                     elif ("name_en" in row and searchString == row["name_en"]):
#                         name = row["name_en"]
#                     else:
#                         name = row["label"]
#
#                     # remove whitespaces at the end of string (for duplicate detection)
#                     name = name.strip()
#                     items.append({"name": name})
#
#         from django.db import connection
#
#         cursor = connection.cursor()
#
#         searchString = searchString.replace(".", "", 2)
#         searchString = searchString.replace(" ", "", 2)
#
#         cursor.execute("""SELECT search_string FROM geodata.search_index_v
#                           WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper(%(search_string)s)
#                           GROUP BY search_string
#                           ORDER BY search_string DESC, length(search_string) LIMIT 100""",
#                        {"search_string": "%" + searchString + "%"})
#
#         rows = cursor.fetchall()
#         #return HttpResponse(cursor.query)
#
#         for row in rows:
#             item = {'name': row[0].strip()}
#             items.append(item)
#         # ===========================================================================
#         # END local data
#
#         # remove duplicate entries
#
#         output = []
#         for x in items:
#             if x not in output:
#                 output.append(x)
#         # return HttpResponse(request.GET["callback"] + "(" + json.dumps({'result': output}) + ")")
#         return Response(output)