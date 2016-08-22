# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import psycopg2
import time

def test_null(invalue):

    outval = None
    outval = invalue

    if invalue == "":
        outval = 'NULL'
    if invalue == " ":
        outval = 'NULL'
    if invalue == "\\None":
        outval = 'NULL'
    if invalue == 'None':
        outval = 'NULL'
    if invalue == None:
        outval = 'NULL'

    if outval == None:
        return outval
    else:
        if isinstance(invalue,str):
            return invalue.replace("'", "''")
        else:
            return invalue

startscript = time.time()  # we will use this later


conn1 = psycopg2.connect(host='localhost', user='postgres', port='5434', password='air', database='wu_old_db')
cur1 = conn1.cursor()
# cur2.execute("select building, geom from geodata.og01_umriss")
# f = cur2.fetchall()
# print(f)

conn2 = psycopg2.connect(host='localhost', user='indrz-wu', port='5434', password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
cur2 = conn2.cursor()



pg_schema = ('geodata')
table_abrev = ('ug01_', 'eg00_', 'og01_', 'og02_', 'og03_', 'og04_', 'og05_', 'og06_' )
floor_values = ('poi', 'rooms', 'umriss', 'networklines', 'carto_lines', 'doors', 'furniture' )
other_tables = ('parking_garage', 'raumlist_buchungsys', 'temp_wu_personal_data' )
outdoor_tables = ('od_all_fill', 'od_all_polygons', 'od_baeume_linien', 'od_blindeleitlinie', 'od_fahrradstellplatz', 'od_familie_linie',
                  'od_orientierungselemente_linie', 'od_raucherzone', 'od_relax_area')
bibliothek_tables = ('bibliothek')

building_ids = {'EA': 1, 'D5': 6, 'AD':5, 'LC': 2, 'D1': 7, 'D2': 10, 'D3': 4, 'D4': 3, 'SC': 9, 'TC': 8}

space_type_id_map = {'Drucker': 69,  }

rooms_cols = ('refname', 'room_name', 'room_number', 'building', 'floor', 'description', 'geom', 'building_number',
              'aks_nummer', 'entrance_poi_id', 'room_code', 'category_en' )

indrz_spaces_cols = {'short_name': rooms_cols[1], 'geom': rooms_cols[6], 'room_number': rooms_cols[2],
                      'room_external_id': rooms_cols[8], 'room_number_sign': rooms_cols[10],
                     'fk_space_type_id': rooms_cols[11]}

carto_lines_cols = ('layer', 'refname', 'building', 'floor', 'type', 'geom')

furniture_cols = ('layer', 'refname', 'building', 'floor', 'geom')

doors_cols = ('layer', 'refname', 'building', 'floor', 'geom')


def import_carto_lines(floor_abr):

    """

    :param floor_abr: floor abreviation og02_  for example
    :return:
    """
    for building_abr, building_id in building_ids.items():
        if building_abr:
            floor_level_txt = floor_abr[3:4]
            print('now working on floor: ' + str(floor_level_txt))

            sel_spaces_new = """
                SELECT  lines.type,
                    ST_TRANSFORM(lines.geom, 3857) as geom
                FROM geodata.{0}carto_lines AS lines,
                 geodata.buildings_buildingfloor AS floor
                 WHERE st_within(lines.geom,floor.geom)
                 AND floor.fk_building_id = {1}
                 AND floor.floor_num = {2}

                """.format(floor_abr, building_id, floor_level_txt)
            # print(sel_spaces_new)
            cur1.execute(sel_spaces_new)
            res = None
            res = cur1.fetchall()
            floor_level_txt = floor_abr[3:4]
            print("now on floor level: " + str(floor_level_txt))
            # print(len(res))
            # print(res)
            # print("the type is a " + str(type(res)))
            print("number of features to process: " + str(len(res)))
            if len(res) > 0:

                for r in res:


                    m_types = test_null(r[0])

                    # print("room_name is : " + str(m_types))
                    m_geom = test_null(r[1])


                    sel_building_floor_id = """SELECT id, floor_num, fk_building_id from django.buildings_buildingfloor
                              WHERE floor_num = {0} and fk_building_id = {1}""".format(floor_level_txt, building_id)
                    # print(sel_building_floor_id)

                    cur2.execute(sel_building_floor_id)
                    res_floor_id = cur2.fetchall()
                    # print(res_floor_id)

                    if res_floor_id:
                        # print(res_floor_id)
                        m_floor_id_value = res_floor_id[0][0]
                        # print(m_floor_id_value)
                        # print("FLOOR ID : " + str(m_floor_id_value))
                        if m_floor_id_value > 79:
                            print("we have a problem houston")

                        insert_state = """INSERT INTO django.buildings_buildingfloorplanline (short_name, floor_num,
                            fk_building_id, fk_building_floor_id, geom)
                                    VALUES (\'{0}\', \'{1}\', {2}, \'{3}\',\'{4}\'  )""".format(m_types, floor_level_txt,
                                                                               building_id, m_floor_id_value, m_geom)
                        cur2.execute(insert_state)
                        conn2.commit()

                print('done inserting on building id: ' + str(building_id))



# for floor in table_abrev:
#     import_carto_lines(floor)


def import_furniture(floor_abr):

    """

    :param floor_abr: floor abreviation og02_  for example
    :return:
    """
    for building_abr, building_id in building_ids.items():
        if building_abr:
            floor_level_txt = floor_abr[3:4]
            print('now working on floor: ' + str(floor_level_txt))

            sel_spaces_new = """
                SELECT  lines.refname,
                    ST_TRANSFORM(lines.geom, 3857) as geom
                FROM geodata.{0}furniture AS lines,
                 geodata.buildings_buildingfloor AS floor
                 WHERE st_within(lines.geom,floor.geom)
                 AND floor.fk_building_id = {1}
                 AND floor.floor_num = {2}

                """.format(floor_abr, building_id, floor_level_txt)
            # print(sel_spaces_new)
            cur1.execute(sel_spaces_new)
            res = None
            res = cur1.fetchall()
            floor_level_txt = floor_abr[3:4]
            print("now on floor level: " + str(floor_level_txt))
            # print(len(res))
            # print(res)
            # print("the type is a " + str(type(res)))
            print("number of features to process: " + str(len(res)))
            if len(res) > 0:

                for r in res:


                    m_types = test_null(r[0])

                    # print("room_name is : " + str(m_types))
                    m_geom = test_null(r[1])


                    sel_building_floor_id = """SELECT id, floor_num, fk_building_id from django.buildings_buildingfloor
                              WHERE floor_num = {0} and fk_building_id = {1}""".format(floor_level_txt, building_id)
                    # print(sel_building_floor_id)

                    cur2.execute(sel_building_floor_id)
                    res_floor_id = cur2.fetchall()
                    # print(res_floor_id)

                    if res_floor_id:
                        # print(res_floor_id)
                        m_floor_id_value = res_floor_id[0][0]
                        # print(m_floor_id_value)
                        # print("FLOOR ID : " + str(m_floor_id_value))
                        if m_floor_id_value > 79:
                            print("we have a problem houston")

                        insert_state = """INSERT INTO django.buildings_buildingfloorplanline (short_name, long_name, floor_num,
                            fk_building_id, fk_building_floor_id, geom)
                                    VALUES ('furniture',\'{0}\', \'{1}\', {2}, \'{3}\',\'{4}\'  )""".format(m_types, floor_level_txt,
                                                                               building_id, m_floor_id_value, m_geom)
                        cur2.execute(insert_state)
                        conn2.commit()

                print('done inserting on building id: ' + str(building_id))



for floor in table_abrev:
    import_furniture(floor)

def import_doors(floor_abr):

    """

    :param floor_abr: floor abreviation og02_  for example
    :return:
    """
    for building_abr, building_id in building_ids.items():
        if building_abr:
            floor_level_txt = floor_abr[3:4]
            print('now working on floor: ' + str(floor_level_txt))

            sel_spaces_new = """
                SELECT  lines.layer,
                    ST_TRANSFORM(lines.geom, 3857) as geom
                FROM geodata.{0}doors AS lines,
                 geodata.buildings_buildingfloor AS floor
                 WHERE st_within(lines.geom,floor.geom)
                 AND floor.fk_building_id = {1}
                 AND floor.floor_num = {2}

                """.format(floor_abr, building_id, floor_level_txt)
            # print(sel_spaces_new)
            cur1.execute(sel_spaces_new)
            res = None
            res = cur1.fetchall()
            floor_level_txt = floor_abr[3:4]
            print("now on floor level: " + str(floor_level_txt))
            # print(len(res))
            # print(res)
            # print("the type is a " + str(type(res)))
            print("number of features to process: " + str(len(res)))
            if len(res) > 0:

                for r in res:


                    m_types = test_null(r[0])

                    # print("room_name is : " + str(m_types))
                    m_geom = test_null(r[1])


                    sel_building_floor_id = """SELECT id, floor_num, fk_building_id from django.buildings_buildingfloor
                              WHERE floor_num = {0} and fk_building_id = {1}""".format(floor_level_txt, building_id)
                    # print(sel_building_floor_id)

                    cur2.execute(sel_building_floor_id)
                    res_floor_id = cur2.fetchall()
                    # print(res_floor_id)

                    if res_floor_id:
                        # print(res_floor_id)
                        m_floor_id_value = res_floor_id[0][0]
                        # print(m_floor_id_value)
                        # print("FLOOR ID : " + str(m_floor_id_value))
                        if m_floor_id_value > 79:
                            print("we have a problem houston")

                        insert_state = """INSERT INTO django.buildings_buildingfloorplanline (short_name, long_name, floor_num,
                            fk_building_id, fk_building_floor_id, geom)
                                    VALUES ('door',\'{0}\', \'{1}\', {2}, \'{3}\',\'{4}\'  )""".format(m_types, floor_level_txt,
                                                                               building_id, m_floor_id_value, m_geom)
                        cur2.execute(insert_state)
                        conn2.commit()

                print('done inserting on building id: ' + str(building_id))



for floor in table_abrev:

    import_doors(floor)

endscript = time.time()
endtime = endscript - startscript
print ('script run in ' + str(endscript - startscript) + ' seconds or ' + '\n'
       + str((endscript - startscript)*1000) + ' miliseconds')
