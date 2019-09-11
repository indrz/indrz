import pandas as pd
import os
from django.contrib.gis.gdal import DataSource, SpatialReference
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon


import psycopg2
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_pass = os.getenv('DB_PASSWORD')

con_string = f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"
conn = psycopg2.connect(con_string)
cur = conn.cursor()


# pnt = GEOSGeometry('POINT(5 23)')
# pnt_v2= Point(5,23)
# print(GEOSGeometry('POINT (0 0)', srid=4326))
# geo_pt = Point(row['Position X'], row['Position Y'], srid=31259)

def get_dxf_fullpath(campus, dxf_file_name):
    dxf_dir_path = Path('c:/Users/mdiener/GOMOGI/TU-indrz - Dokumente/dwg-working/' + campus)

    dxf_file_full_path = Path.joinpath(dxf_dir_path, dxf_file_name)

    return dxf_file_full_path



def is_roomcode(value):
    unique_floor_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO',
                          'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']
    if value:
        if type(value) is str:
            # print("ROOM NUMBER IS ", room_n, floor_name)indrz_lines_03
            if len(value.split(' ')) == 3 :
                if value.split(' ')[1] in unique_floor_names:
                    floor_name = value.split(' ')[1]
                    trak_code = value.split(' ')[0]
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False




def get_floor_name(room_n, room_c, room_v):
    unique_floor_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'DG', 'EG', 'SO',
                          'U1', 'U2', 'U3', 'U4', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'ZD', 'ZE', 'ZU']

    floor_name = ""
    trak_code = ""

    if room_n:
        if type(room_n) is str:
            # print("ROOM NUMBER IS ", room_n, floor_name)indrz_lines_03
            if len(room_n.split(' ')) == 3 :
                if room_n.split(' ')[1] in unique_floor_names:
                    floor_name = room_n.split(' ')[1]
                    trak_code = room_n.split(' ')[0]
    if room_c:
        if type(room_c) is str:
            if len(room_c.split(' ')) == 3 :
                if room_c.split(' ')[1] in unique_floor_names:
                    floor_name = room_c.split(' ')[1]
                    trak_code = room_c.split(' ')[0]
    if room_v:
        if type(room_v) is str:
            if len(room_v.split(' ')) == 3 :
                if room_v.split(' ')[1] in unique_floor_names:
                    floor_name = room_v.split(' ')[1]
                    trak_code = room_v.split(' ')[0]

    return floor_name, trak_code


def read_campus_csv_list(campus, re_import=False):
    csv_file_name = campus.lower() + "_roomcodes.csv"

    csv_filepath = get_dxf_fullpath('Arsenal', csv_file_name)

    # df = pd.read_csv(csv_filepath, names=["Name","Position X","Position Y","RAUMBEZEICHNUNG","RAUMNUMMER","Value", "Layer", "RAUMCODE", "RAUMNR"], delimiter=",")

    df = pd.read_csv(csv_filepath, delimiter=",", error_bad_lines=False)


    print(df.columns)

    if re_import:
        print("now removing old points in db")
        dxf_layer_name = ""
        sql_delete_s = F"DELETE FROM campuses.indrz_imported_roomcodes CASCADE WHERE tags[1] = '{dxf_layer_name}'"
        print(sql_delete_s)
        cur.execute(sql_delete_s)
        conn.commit()


    print(df.count)
    # remove all rows where x coord is null
    df = df[df['Position X'].notnull()]


    print(df.count)
    # remove all rows where x coord is invalid like 43.23
    df = df[df['Position X'] > 700000]

    print(df.count)

    # get unique list of room descriptions

    # v = ['WC', 'GANG', 'STG', 'STIEGE',  'AUFZUG', 'BÜRO']
    # grouped_campus = df.groupby('RAUMBEZEICHNUNG')
    # gc = [name for name, group in grouped_campus]
    # print("unique raumbez ", len(gc))
    # print(gc)

    for index, row in df.iterrows():
        cad_layer = row['Layer']
        x = row['Position X']
        y = row['Position Y']
        room_des = row['RAUMBEZEICHNUNG']
        room_n = row['RAUMNUMMER'] # this is used as the roomcode
        room_c = row['RAUMCODE']
        room_nr = row['RAUMNR']
        room_v = row['Value']
        floor_name = ""
        track_code = ""

        floor_name, trak_code = get_floor_name(room_n, room_c, room_v)

        geom_sql = f"ST_SetSRID(ST_MakePoint({x}, {y}), 31259)"

        sql = f"""INSERT INTO campuses.indrz_imported_roomcodes (campus, cad_layer_name, floor_name, room_description,
                            room_external_id, room_number, room_code, room_text, geom)
                    VALUES ('{campus}', '{cad_layer}', '{floor_name}','{room_des}',
                          '{room_n}', '{room_nr}', '{room_c}', '{room_v}', {geom_sql})"""

        print(sql)


        cur.execute(sql)
        conn.commit()

        # sql_clean = """DELETE FROM campuses.indrz_imported_roomcodes
        #     WHERE  """



# read_campus_csv_list('Arsenal')



def determine_code(campus, floor):

    # sql_space = f"""SELECT id, geom FROM campuses.indrz_spaces_{floor}; """

    sql_space = f""" SELECT DISTINCT s.id, s.tags, ST_asewkt(s.geom)
                    FROM campuses.indrz_spaces_{floor} as s
                    JOIN campuses.indrz_imported_roomcodes as p
                    ON ST_Intersects(s.geom, p.geom)
                    WHERE p.floor_name = '{floor}';"""

    sql_pts = f"""SELECT p.id, p.campus, p.floor_name, p.room_external_id, p.room_code, p.room_text, p.geom, p.room_description
                    FROM campuses.indrz_imported_roomcodes as p
                    JOIN campuses.indrz_spaces_{floor} as s
                    ON ST_Intersects(s.geom, p.geom)
                    WHERE p.floor_name = '{floor}';"""
                    # AND p.room_external_id != 'nan';"""

    cur.execute(sql_space)
    spaces = cur.fetchall()

    p = cur.execute(sql_pts)
    points = cur.fetchall()

    print("spaces len ", len(spaces))
    print("points len ", len(points))

    # for point in points:
    #     print(point)

    pts_in = []
    pts_with_id = []
    total_spaces_udated = []

    # list of spaces with 1 or more points inside
    for space in spaces:
        space_geom = GEOSGeometry(space[2])
        space_id = space[0]

        done = False

        for point in points:
            pt_geom = GEOSGeometry(point[6])

            if pt_geom.within(space_geom):
                # print("your are in ", point)

                ext_id = point[3]
                room_des = point[7]
                room_code = point[4]

                # prio 1 if not nan take value and move on
                if ext_id != 'nan':

                    pts_with_id.append(point)
                    update_sql = f"""UPDATE campuses.indrz_spaces_{floor.lower()} 
                                    SET room_external_id = '{ext_id}', room_description = '{room_des}' 
                                    WHERE id = {space_id};"""
                    print(update_sql)

                    cur.execute(update_sql)
                    conn.commit()

                    total_spaces_udated.append(space_id)

                    done = True
                    break
                elif is_roomcode(room_code) and room_code != 'nan':
                    update_sql = f"""UPDATE campuses.indrz_spaces_{floor.lower()} SET room_external_id = '{room_code}'
                                        WHERE id = {space_id};"""
                    print(update_sql)

                    cur.execute(update_sql)
                    conn.commit()
                    done = True

                    total_spaces_udated.append(space_id)
                    break

                pts_in.append(point)
        if done:
            continue

    print("total updated is ", len(total_spaces_udated), total_spaces_udated)



determine_code('Arsenal', 'U2')
conn.close()

    # priority 1 CASE 1
    # POINT is INSIDE a SPACE Polygon

    # if 1 point in polygon
    # if room_external_id has a value this takes priority  source cad layer GUT_RAUMSTEMPL
    # else check
    # if 1 or more points in  space and both have this filled take first one
    # if 1 or more points in space and only one has filled take it and move on ignore other

    # case 2 Multiple points in one space
    # a room_external_id value is good :)  take it move on

    # case 3 Multiple points in once space
    # room_external_id value empty
    # check room_code if good take it
    # if room_code empty check room_text if good take it

    # else bail no data

    # GUT_RAUMSTEMPLE has no roomcode
