#!/bin/python
# coding: utf-8
import psycopg2
import time

building_ids = {'EA': 1, 'D5': 6, 'AD':5, 'LC': 2, 'D1': 7, 'D2': 10, 'D3': 4, 'D4': 3, 'SC': 9, 'TC': 8}
table_abrev = ('ug01_', 'eg00_', 'og01_', 'og02_', 'og03_', 'og04_', 'og05_', 'og06_' )


# conn1 = psycopg2.connect(host='localhost', user='postgres', port='5434', password='air', database='wu_old_db')
# cur1 = conn1.cursor()
# # cur2.execute("select building, geom from geodata.og01_umriss")
# # f = cur2.fetchall()
# # print(f)
#
#
# conn2 = psycopg2.connect(host='localhost', user='indrz-wu', port='5432', password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
# cur2 = conn2.cursor()


conn1 = psycopg2.connect(host='localhost', user='postgres', port='5434', password='air', database='wu_old_db')
cur1 = conn1.cursor()
# cur2.execute("select building, geom from geodata.og01_umriss")
# f = cur2.fetchall()
# print(f)



conn2 = psycopg2.connect(host='gis-neu.wu.ac.at', user='indrz-wu', port='5432', password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
cur2 = conn2.cursor()

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


def test_call(floor_abr):

    disabled_items = []
    for building_abr, building_id in building_ids.items():

        if building_abr:
            floor_level_txt = floor_abr[3:4]
            # print('now working on floor: ' + str(floor_level_txt))

            sel_spaces_new = """
                SELECT  poi.description_en, poi.cat_main_en, poi.cat_sub_en, poi.icon_name_css, poi.sort_order,
                    ST_MULTI(ST_TRANSFORM(poi.geom, 3857)) as geom, poi.aks_nummer
                FROM geodata.{0}poi AS poi,
                 geodata.buildings_buildingfloor AS floor
                 WHERE st_within(poi.geom,floor.geom)
                 AND floor.fk_building_id = {1}
                 AND floor.floor_num = {2}
                 AND poi.enabled = 1

                """.format(floor_abr, building_id, floor_level_txt)
            # print(sel_spaces_new)
            cur1.execute(sel_spaces_new)
            res = None
            res = cur1.fetchall()
            # floor_level_txt = floor_abr[3:4]
            # print("now on floor level: " + str(floor_level_txt))
            # print("now on floor level: " + str(floor_level_txt))

            for r in res:
                disabled_items.append(r)
                poi_name = test_null(r[0])

                # print("room_name is : " + str(m_types))
                m_geom = test_null(r[5])

                poi_descript = test_null(r[6])

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

                    # sel_poi_dis = """SELECT name, floor_num, fk_building_floor_id, fk_campus_id, fk_building_id, fk_poi_category_id, geom, description
                    # from django.poi_manager_poi
                    # WHERE st_equals(geom,\'{0}\')""".format(m_geom)


                    updated_poi_dis = """UPDATE django.poi_manager_poi set enabled = TRUE
                          WHERE st_equals(geom,\'{0}\')""".format(m_geom)


                    print(updated_poi_dis)
                    cur2.execute(updated_poi_dis)
                    conn2.commit()

    return disabled_items

total_dis = []

for floor in table_abrev:

    num_items = test_call(floor)

    total_dis.append(num_items)



print(total_dis[0])
# print(len(total_dis))

sum = 0
for x in total_dis:
    sum += len(x)
    print(len(x))
print(sum)
