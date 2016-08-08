# Create your views here.
import json
import re

from rest_framework.response import Response


def rvk_call(request, q):
    """
    if a space was used in the url it is encoded as %20
    :param request:
    :param q:
    :return:
    """
    # rvk_key = q.replace('%20', '_')
    rvk_key = q['key'].replace('%20', '_')
    rvk_key = rvk_key.upper()

    if re.match(
            "[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-](([0-9]{1,5})|([A-Za-z]([0-9]{1,5})?)))?[ _]*[a-zA-Z][0-9]{1,3}.*",
            rvk_key):
        #query fo08r searching the shelf, this first part remains the same all the time
        sql = 'select * from library.shelf_data where main_cat = %(cat_main)s  and sub_cat = %(cat_sub)s and numbers <= cast(%(numbers)s as int)'

        #regex saves named parameters (eg. ?P<cat_main>) in the regDict. you can access it with regDict["cat_main"]
        regex = "(?P<cat_main>[a-zA-Z])"                    #cat_main
        regex += "(?:(?P<cat_sub>[a-zA-Z]))?"                #optional cat_sub
        regex += "[ _]*(?P<numbers>[0-9]{3,5})"                #numbers
        regex += "((?P<postNumbers>[-\.][0-9]{1,5})|(?P<postChar>[\.\-][A-Za-z])|((?P<postCharNumbers_Char>[\.\-][A-Za-z])(?P<postCharNumbers_Number>[0-9]{1,6})))?"
        regex += "[ _]*(?P<author>[a-zA-Z][ _]*[0-9]{1,3}).*" #author and rest

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
            regDict["postNumbers"] = regDict["postNumbers"][1:] # cut off first char which is the "-"
            sql += "and numbers_2 <= %(postNumbers)s and charnumber_char is null and charnumber_digit = 0"

        # .char
        elif re.match("[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-][a-zA-Z])[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*", rvk_key):
            regDict["postChar"] = regDict["postChar"][1:] # cut off first char which is the "-"
            sql += " and numbers_2 = 0 and charnumber_char is not null and charnumber_char <= %(postChar)s and charnumber_digit = 0"

        # .char + numbers
        elif re.match("[a-zA-Z][a-zA-Z]?[ _]*[0-9]{3,5}([\.\-][a-zA-Z][0-9]{1,6})[ _]+[a-zA-Z][ _]*[0-9]{1,3}.*",
                      rvk_key):
            regDict["postCharNumbers_Char"] = regDict["postCharNumbers_Char"][1:] # cut off first char which is the "-"
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

            if(len(dbrow) > 0):
                # =======================================================================================
                # first find the right shelf (ignore author if result numbers < numbers, since it will contain everything; else search for shelf starting with author < request author)
                i = 0
                numbers = dbrow[0][5]
                author = dbrow[0][9]

                if int(numbers) == int(regDict["numbers"]):
                    while (author[:1] > regDict["author"][:1]) or (author[:1] == regDict["author"][:1] and int(author[1:]) > int(regDict["author"][1:])):
                        i = i+1
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
                sql = "SELECT shelf_area FROM library.shelfdata where shelf_id = \'" + shelfID + "\' and floor = \'" + floor + "\' GROUP BY shelf_area;"
                cursor.execute(sql)
                length = len(cursor.fetchall())

                # index of section divided through number of sections, minus 0,5 * length of section
                # (so we are in the middle of the section) and the whole thing *2 (in sql query), since we have 2 sides.
                # (ord(shelfArea) gives the ascii value of the character, eg a = 97, b = 98,...
                # (ord(shelfArea)-96 --> a = 1, b = 2, c = 3...
                # we do this to get the position of the shelf-area.
                sideIndicator = float((ord(shelfArea) - 96)) / float(length)
                sectionPosition = (float((ord(shelfArea) - 96)) / float(length) - 0.5 / float(length))

                #========================================================================================

                # now get the geometry of the shelf
                # no sql injection possible since data comes from regex-view and is guaranteed to be in the right format.
                # sql = "select  ST_AsGeoJson(ST_Force_2d(geom)) from geodata.og0" + building[3:4] +
                # "_library_regal_lines where id_letter = \'" + shelfID + "\';"

                sql = "select ST_AsGeoJson(ST_Line_Interpolate_Point(ST_OffsetCurve((select geom from geodata.og0" + building[3:4] + "_library_regal_lines where id_letter = \'" + shelfID + "\'),"
                
                if sideIndicator > 0.5:
                    sql += "-0.7), " + str(1 - (1 - sectionPosition) * 2) + "))"
                else:
                    sql += "0.7), " + str(sectionPosition * 2) + "))"

                cursor.execute(sql)
                dbrow = cursor.fetchall()
                if(len(dbrow) > 0):
                    geom = dbrow[0][0]
                    geomJson = json.loads(str(geom))

                    # get the highlighted geometry of the shelf
                    sql = "select ST_AsGeoJson(geom) from geodata.og0" + building[3:4] + "_library_shelf_poly where id_letter = \'" + shelfID + "\';"
                    cursor.execute(sql)
                    dbrow = cursor.fetchall()

                    shelfGeom = dbrow[0][0]
                    shelfGeomJson = json.loads(str(shelfGeom))

                    item = {
                        "type": "Feature",
                        "properties":
                            {
                                "text": rvk_key,
                                "building": building[:2],
                                "floor": building[3:4],
                                "shelfID": shelfID,
                                "fachboden": fachboden,
                                "position": str(sectionPosition),
                            },
                        "geometry": geomJson,
                        "shelfGeometry": shelfGeomJson
                    }
                else: 
                    return Response(None)
            else: 
                return Response(None)

        # execute query stuff end
        # ============================================================================================
        return Response(item)
    # return HttpResponse(returnVal)
    else:
        return Response(None)