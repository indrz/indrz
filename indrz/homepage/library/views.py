# Create your views here.
import json
import re
from geojson import Feature, FeatureCollection

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def rvk_call(request, rvk_id):
    """
    if a space was used in the url it is encoded as %20
    :param request:
    :param q:
    :return:
    """
    # rvk_key = q.replace('%20', '_')
    # rvk_key = rvk_id['key'].replace('%20', '_')
    # rvk_key = rvk_id.replace('%20', '_')
    # print(rvk_id)
    rvk_key = rvk_id.upper()
    # print(rvk_key)

    if re.match(
            "[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-](([0-9]{1,5})|([A-Za-z]([0-9]{1,5})?)))?[ _]*[a-zA-Z][0-9]{1,3}.*",
            rvk_key):
        # query fo08r searching the shelf, this first part remains the same all the time
        sql = 'SELECT * FROM library.shelf_data WHERE main_cat = %(cat_main)s  AND sub_cat = %(cat_sub)s AND numbers <= CAST(%(numbers)s AS INT)'

        # regex saves named parameters (eg. ?P<cat_main>) in the regDict. you can access it with regDict["cat_main"]
        regex = "(?P<cat_main>[a-zA-Z])"  # cat_main
        regex += "(?:(?P<cat_sub>[a-zA-Z]))?"  # optional cat_sub
        regex += "[ _]*(?P<numbers>[0-9]{3,5})"  # numbers
        regex += "((?P<postNumbers>[-\.][0-9]{1,5})|(?P<postChar>[\.\-][A-Za-z])|((?P<postCharNumbers_Char>[\.\-][A-Za-z])(?P<postCharNumbers_Number>[0-9]{1,6})))?"
        regex += "[ _]*(?P<author>[a-zA-Z][ _]*[0-9]{1,3}).*"  # author and rest

        # match the regex and save the named parameters in regDict (Dictionary)
        regexList = re.match(regex, rvk_key)
        regDict = regexList.groupdict()

        # ========================================================================================
        # CASES FOR SEARCH VALUE

        # normal
        if re.match("[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*", rvk_key):
            # ignore sections with numbers_2 or charnumber set (the thingies after the dot, or in the url after minus )
            sql += " and numbers_2 = 0 and charnumber_char is null and charnumber_digit = 0"

        # .numbers
        elif re.match("[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-][0-9]{1,5})?[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*", rvk_key):
            regDict["postNumbers"] = regDict["postNumbers"][1:]  # cut off first char which is the "-"
            sql += "and numbers_2 <= %(postNumbers)s and charnumber_char is null and charnumber_digit = 0"

        # .char
        elif re.match("[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-][a-zA-Z])[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*", rvk_key):
            regDict["postChar"] = regDict["postChar"][1:]  # cut off first char which is the "-"
            sql += " and numbers_2 = 0 and charnumber_char is not null and charnumber_char <= %(postChar)s and charnumber_digit = 0"

        # .char + numbers
        elif re.match("[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-][a-zA-Z][0-9]{1,6})[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*",
                      rvk_key):
            regDict["postCharNumbers_Char"] = regDict["postCharNumbers_Char"][1:]  # cut off first char which is the "-"
            sql += " and numbers_2 = 0 and charnumber_char is not null and charnumber_char <= %(postCharNumbers_Char)s and charnumber_digit <= cast(%(postCharNumbers_Number)s as int)"

        # CASES FOR SEARCH VALUE END
        # ========================================================================================

        # add author search
        sql += ' order by numbers desc, numbers_2 desc, charnumber_char desc, charnumber_digit desc, row_number desc;'
        # ========================================================================================
        # execute query

        from django.db import connection

        cursor = connection.cursor()

        if cursor is not None:
            cursor.execute(sql, regDict)

            # return HttpResponse(cursor.query)


            dbrow = cursor.fetchall()

            if (len(dbrow) > 0):
                # =======================================================================================
                # first find the right shelf (ignore author if result numbers < numbers, since it will contain everything; else search for shelf starting with author < request author)
                i = 0
                numbers = dbrow[0][5]
                author = dbrow[0][9]

                if int(numbers) == int(regDict["numbers"]):
                    while (author[:1] > regDict["author"][:1]) or (
                            author[:1] == regDict["author"][:1] and int(author[1:]) > int(regDict["author"][1:])):
                        i = i + 1
                        numbers = dbrow[i][5]
                        author = dbrow[i][9]

                shelfID = dbrow[i][10]
                shelfArea = dbrow[i][11]
                fachboden = dbrow[i][12]
                building = dbrow[i][15]
                floor = dbrow[i][14]

                # =======================================================================================
                # find out on which side of the shelf the section is. < 0.5: left, > 0.5: right
                # 1st get the number of sections
                sql = "SELECT shelf_area FROM library.shelfdata WHERE shelf_id = \'" + shelfID + "\' AND floor = \'" + floor + "\' GROUP BY shelf_area;"
                cursor.execute(sql)
                length = len(cursor.fetchall())

                # index of section divided through number of sections, minus 0,5 * length of section
                # (so we are in the middle of the section) and the whole thing *2 (in sql query), since we have 2 sides.
                # (ord(shelfArea) gives the ascii value of the character, eg a = 97, b = 98,...
                # (ord(shelfArea)-96 --> a = 1, b = 2, c = 3...
                # we do this to get the position of the shelf-area.
                sideIndicator = float((ord(shelfArea) - 96)) / float(length)
                sectionPosition = (float((ord(shelfArea) - 96)) / float(length) - 0.5 / float(length))

                # ========================================================================================

                # now get the geometry of the shelf
                # no sql injection possible since data comes from regex-view and is guaranteed to be in the right format.
                # sql = "select  ST_AsGeoJson(ST_Force_2d(geom)) from geodata.og0" + building[3:4] +
                # "_library_regal_lines where id_letter = \'" + shelfID + "\';"

                sql = "SELECT ST_AsGeoJson(ST_Line_Interpolate_Point" \
                      "(ST_OffsetCurve((SELECT geom FROM library.og0" + building[3:4] +\
                      "_library_regal_lines WHERE id_letter = \'" + shelfID + "\'),"

                if sideIndicator > 0.5:
                    sql += "-0.7), " + str(1 - (1 - sectionPosition) * 2) + "))"
                else:
                    sql += "0.7), " + str(sectionPosition * 2) + "))"

                cursor.execute(sql)
                dbrow = cursor.fetchall()
                if (len(dbrow) > 0):
                    geom = dbrow[0][0]
                    geomJson = json.loads(str(geom))

                    # get the highlighted geometry of the shelf
                    sql = "SELECT ST_AsGeoJson(geom) FROM library.og0" + building[3:4] +\
                          "_library_shelf_poly WHERE id_letter = \'" + shelfID + "\';"

                    cursor.execute(sql)
                    dbrow = cursor.fetchall()

                    shelfGeom = dbrow[0][0]
                    shelfGeomJson = json.loads(str(shelfGeom))
                    shelf_properties = {
                        "text": rvk_key,
                        "building": building[:2],
                        "floor": building[3:4],
                        "shelfID": shelfID,
                        "fachboden": fachboden,
                        "position": str(sectionPosition),
                    }
                    point_location = Feature(geometry=geomJson, properties=shelf_properties)
                    shelf_poly = Feature(geometry=shelfGeomJson, properties=shelf_properties)
                    result_collection = FeatureCollection([shelf_poly, point_location])

                    return Response(result_collection)

                else:
                    return Response({'error 4': 'len db row is 0'})
            else:
                return Response({'error 3': 'no rvk found in first query'})

        # execute query stuff end
        # ============================================================================================
        return Response({'error 2': 'query to DB returned nothing hmm'})
    # return HttpResponse(returnVal)
    else:
        return Response({'error 1': 'boom the RVK code does not match sorry call us'})


@api_view(['GET'])
def route_to_book(request, rvk_id):
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
        # localhost:8000/api/v1/directions/1826545.2173675,6142423.4241214,0&1826600.05182995,6142427.76651319,5
