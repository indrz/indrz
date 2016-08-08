# search anything on campus
import json
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
        rows.append(obj)

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
        entranceID = results[0][0];

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


# @jsonrpc_method('searchAny(q=dict) -> dict', validate=True)
@api_view(['GET'])
def search_any(request, q):
    if q.keys().index('searchString') < 0:
        raise Exception("Couldn't find searchString in parameter q")
    searchString = q['searchString']

    # dont allow empty searchString, too short searchString or too long searchstring (50 characters is way too much
    #  and probably a sql attack so we prevent it here aswell
    if searchString == "" or len(searchString) < 2 or len(searchString) > 100:
        raise Exception("searchString is too short. Must be at least 2 characters")

    # check for possible sql attacks etc...
    if '}' in searchString or '{' in searchString or ';' in searchString:
        raise Exception("illegal characters in searchString")

    extraBuilding = ''

    # rows-array which will contain the return dataset
    rows = []

    from django.db import connection

    cursor = connection.cursor()

    # if searchSTring contains a comma, we need to split it and use what is after the comma as building
    # if ',' in searchString:
    #   tmpArr = searchString.partition(',')
    #   searchString = tmpArr[0]
    #   extraBuilding = tmpArr[2].strip()

    # searchString can be used for SQL injections - to prevent this we are using the
    # cursor.execute method with searchString as parameter
    # sql = basicQuery = """
    # select search_string, text_type, external_id, st_asgeojson(geom) as geom,
    # st_asgeojson(st_PointOnSurface(geom)) as center, layer, building, 0 as resultType, aks_nummer
    #       FROM geodata.search_index_v
    #       WHERE upper(building) LIKE %(building)s AND ( upper(search_string) LIKE %(search_string)s
    #       OR aks_nummer LIKE %(search_string)s )
    #       ORDER BY priority DESC, length(search_string) LIMIT 9
    # """
    sql = basicQuery = """
    SELECT search_string, text_type, external_id, st_asgeojson(geom) AS geom, st_asgeojson(st_PointOnSurface(geom)) AS center, layer, building, 0 AS resultType, aks_nummer, roomcode
            FROM geodata.search_index_v
            WHERE upper(search_string) LIKE %(search_string)s
            ORDER BY priority DESC, length(search_string) LIMIT 9
    """

    # query bach api rooms for room data
    bachData = []
    room_data_results = bach_calls.bach_search_rooms(searchString)
    if room_data_results != None:
        bachData.extend(room_data_results)

    # =============================================
    # extend d organisations and people data in one
    bachOrgs = bach_calls.bach_search_directory(searchString)
    bachData.extend(bachOrgs)
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
                     layer, building, 0 AS resultType, aks_nummer, roomcode \
                     FROM geodata.search_index_v \
                     WHERE aks_nummer = upper(%(location)s)", locationDict)

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
                        if ("name_de" in row and "name_en" in row):
                            name_de = row["name_de"]
                            name_en = row["name_en"]

                        elif ("label" in row):
                            name_de = row["label"]
                            name_en = row["label"]

                        # no name data means we only have room data
                        elif ("roomname_en" in row and "roomname_de" in row):
                            name_en = row["roomname_en"]
                            name_de = row["roomname_de"]

                        elif 'roomcode' in row:
                            roomcode_value = row['roomcode']

                        elif 'category_de' in row:
                            cat_de_value = row['category_de']

                        elif 'category_en' in row:
                            cat_en_value = row['category_en']

                        if cat_de_value is not None:
                            cat_de_encode = cat_de_value.encode('utf-8')
                            cat_en_encode = cat_en_value.encode('utf-8')
                        else:
                            cat_de_encode = ""
                            cat_en_encode = ""
                        # ==========================================================
                        # find out location of frontoffice
                        roomcode_value = repNoneWithEmpty(result[0][9])

                        if roomcode_value == '':
                            roomcode_value = None

                        frontoffice = ""
                        if orgid != None and orgid != "":
                            organization_details = bach_calls.bach_get_organization_details(orgid)
                            if organization_details != None and len(organization_details) > 0:
                                frontoffice = organization_details["location"]

                        obj = {"name_de": name_de,
                               "name_en": name_en,
                               "roomcode_value": roomcode_value,
                               "type": repNoneWithEmpty(result[0][1]),
                               "external_id": repNoneWithEmpty(result[0][2]),
                               "geometry": repNoneWithEmpty(result[0][3]),
                               "centerGeometry": repNoneWithEmpty(result[0][4]),
                               "layer": repNoneWithEmpty(int(result[0][5])),
                               "building": repNoneWithEmpty(result[0][6]),
                               "aks_nummer": repNoneWithEmpty(locationDict["location"]),
                               "orgid": repNoneWithEmpty(orgid),
                               "frontoffice": repNoneWithEmpty(frontoffice),
                               "category_de": repNoneWithEmpty(cat_de_encode),
                               "category_en": repNoneWithEmpty(cat_en_encode),
                               "src": "bach"
                               }

                        bachLocationStrings.append(obj)

                else:
                    # no location from bach api, search in temp table for location:
                    # to do uncomment next to lines when we allow search on people

                    cursor.execute("SELECT aks FROM geodata.temp_wu_personal_data WHERE name LIKE %(searchString)s",
                                   {"searchString": "%" + searchString + "%"})
                    results = cursor.fetchall()

                    if len(results) > 0:
                        for result in results:
                            if result[0] is not None and result[0] != "":
                                cursor.execute("SELECT search_string, text_type, external_id, \
                                 st_asgeojson(geom) AS geom, st_asgeojson(st_PointOnSurface(geom)) AS center, \
                                 layer, building, 0 AS resultType, aks_nummer, roomcode \
                                 FROM geodata.search_index_v \
                                 WHERE aks_nummer = upper(%(location)s)", {"location": result[0]})
                                room = cursor.fetchone()

                                roomcode_value = repNoneWithEmpty(row["roomcode"])

                                if roomcode_value == '':
                                    roomcode_value = None

                                if room is not None:
                                    obj = {"name_de": repNoneWithEmpty(row["label"]),
                                           "name_en": repNoneWithEmpty(row["label"]),
                                           "roomcode_value": repNoneWithEmpty(row["roomcode"]),
                                           "type": repNoneWithEmpty(room[1]),
                                           "external_id": repNoneWithEmpty(room[2]),
                                           "geometry": repNoneWithEmpty(room[3]),
                                           "centerGeometry": repNoneWithEmpty(room[4]),
                                           "layer": repNoneWithEmpty(int(room[5])),
                                           "building": repNoneWithEmpty(room[6]),
                                           "aks_nummer": repNoneWithEmpty(row["location"]),
                                           "orgid": repNoneWithEmpty(row["currentAffiliation"][0]["orgid"]),
                                           "src": "local (no location"}

                                    bachLocationStrings.append(obj)
                                    # else:
                                    # look up orgid and route to frontoffice, currently not in db

    # =================================================================================================================================
    # bach data finished, if entries present --> return them, else do a lookup in our local data.


    if len(bachLocationStrings) > 0:
        # --------------------------------------------------------
        # add the assigned entrance
        for tempResult in bachLocationStrings:
            if (tempResult["aks_nummer"] is not None and tempResult["aks_nummer"] != ""):
                entranceData = getAssignedEntrance(tempResult["aks_nummer"], tempResult["layer"]);
                tempResult["entrance"] = entranceData["id"];
                tempResult["entrance_name_de"] = entranceData["de"];
                tempResult["entrance_name_en"] = entranceData["en"];

        # --------------------------------------------------------
        retVal = {"searchString": searchString, "building": '', "searchResult": bachLocationStrings,
                  "length": bachDataLength}
        return Response(retVal)


    else:
        # query table or view: rooms
        # query columns: room_name
        # Order by similarity? LIMIT to 10
        # need to return: room_name, room_number, coordinates

        # add % at the beginning and end of the search string so we can use it in the like statement
        # also convert searchString toUpper here
        searchString2 = "%" + searchString.upper() + "%"
        extraBuilding2 = "%" + extraBuilding.upper() + "%"

        cursor.execute(sql,
                       {"search_string": searchString2, "building": extraBuilding2,
                        "bach_location_list": tuple(bachLocationStrings)})
        db_rows = cursor.fetchall()

        for row in db_rows:
            loc = row[8]  # row[8] is AKS_NUMMER
            roomcode_value = row[9]  # roomcode

            if roomcode_value == '':
                roomcode_value = None

            if row[7] == 0:  # row[7] = 'resultType'
                # our search string
                obj = {"name_de": row[0], "name_en": row[0], "type": row[1], "external_id": row[2], "geometry": row[3],
                       "centerGeometry": row[4], "layer": int(row[5]), "building": row[6], "aks_nummer": loc,
                       "roomcode_value": roomcode_value,
                       "src": "local"
                       # , "frontoffice": "001_10_OG04_421600", "orgid": "1234"
                       }
            else:
                # bach api location aks number
                locData = bachLocationList[loc]
                if roomcode_value == '':
                    roomcode_value = None
                obj = {"name_de": locData['name_de'], "name_en": locData['name_en'], "type": row[1],
                       "external_id": row[2],
                       "geometry": row[3], "centerGeometry": row[4], "layer": int(row[5]), "building": row[6],
                       "aks_nummer": loc, "roomcode_value": roomcode_value, "src": "local"
                       # , "frontoffice": "001_10_OG04_421600", "orgid": "1234"
                       }
                # end if
            rows.append(obj)

        # --------------------------------------------------------
        # add the assigned entrance
        for tempResult in rows:
            if (tempResult["aks_nummer"] is not None and tempResult["aks_nummer"] != ""):
                entranceData = getAssignedEntrance(tempResult["aks_nummer"], tempResult["layer"]);
                tempResult["entrance"] = entranceData["id"];
                tempResult["entrance_name_de"] = entranceData["de"];
                tempResult["entrance_name_en"] = entranceData["en"];
        # --------------------------------------------------------
        retVal = {"searchString": searchString, "building": extraBuilding, "searchResult": rows, "length": len(db_rows)}

        return Response(retVal)

@api_view(['GET'])
def searchAutoComplete(request):
    searchString = request.GET["query"]
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
                    items.append({"name": name})

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
                    items.append({"name": room_cat})

                elif "category_en" in row and searchString.upper() in row["category_en"].upper():
                    room_cat = row['category_en']
                    room_cat = room_cat.strip()
                    items.append({"name": room_cat})

        # ===========================================================================
        # local Postgresql search_index_v data

        from django.db import connection

        cursor = connection.cursor()

        searchString = searchString.replace(".", "", 2)
        searchString = searchString.replace(" ", "", 2)

        cursor.execute("""SELECT search_string FROM geodata.search_index_v
                          WHERE replace(replace (upper(search_string), '.', ''),'.', '') LIKE upper(%(search_string)s)
                          GROUP BY search_string, priority
                          ORDER BY priority DESC, length(search_string) LIMIT 100""",
                       {"search_string": "%" + searchString + "%"})

        rows = cursor.fetchall()
        # return HttpResponse(cursor.query)

        for row in rows:
            item = {'name': row[0].strip()}
            items.append(item)
        # ===========================================================================
        # END local data

        # remove duplicate entries

        output = []
        for x in items:
            if x not in output:
                output.append(x)
        return HttpResponse(request.GET["callback"] + "(" + json.dumps({'result': output}) + ")")
        # return HttpResponse(json.dumps({'result':items}))