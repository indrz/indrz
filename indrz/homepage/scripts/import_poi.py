#!/bin/python
# coding: utf-8
import psycopg2
import time

building_ids = {'EA': 1, 'D5': 6, 'AD':5, 'LC': 2, 'D1': 7, 'D2': 10, 'D3': 4, 'D4': 3, 'SC': 9, 'TC': 8}
table_abrev = ('ug01_', 'eg00_', 'og01_', 'og02_', 'og03_', 'og04_', 'og05_', 'og06_' )


conn1 = psycopg2.connect(host='localhost', user='postgres', port='5434', password='air', database='wu_old_db')
cur1 = conn1.cursor()
# cur2.execute("select building, geom from geodata.og01_umriss")
# f = cur2.fetchall()
# print(f)

conn2 = psycopg2.connect(host='localhost', user='indrz-wu', port='5434', password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
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

def import_poi(floor_abr):

    """

    :param floor_abr: floor abreviation og02_  for example
    :return:
    """
    for building_abr, building_id in building_ids.items():
        if building_abr:
            floor_level_txt = floor_abr[3:4]
            print('now working on floor: ' + str(floor_level_txt))

            sel_spaces_new = """
                SELECT  poi.description_en, poi.cat_main_en, poi.cat_sub_en, poi.icon_name_css, poi.sort_order,
                    ST_MULTI(ST_TRANSFORM(poi.geom, 3857)) as geom
                FROM geodata.{0}poi AS poi,
                 geodata.buildings_buildingfloor AS floor
                 WHERE st_within(poi.geom,floor.geom)
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


                    poi_name = test_null(r[0])

                    # print("room_name is : " + str(m_types))
                    m_geom = test_null(r[5])


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

                        insert_state = """INSERT INTO django.poi_manager_poi (name, floor_num, fk_building_floor_id,
                                                      fk_campus_id, fk_building_id, fk_poi_category_id, geom)
                                    VALUES (\'{0}\', \'{1}\', {2}, {3},\'{4}\',{5},\'{6}\'  )""".format(poi_name, floor_level_txt, m_floor_id_value,
                                                                               1, building_id, 12, m_geom)
                        print(insert_state)
                        cur2.execute(insert_state)
                        conn2.commit()

                print('done inserting on building id: ' + str(building_id))



for floor in table_abrev:
    import_poi(floor)

poi_name_field_values = {
    "Front Office" : 30,
    "Emergency telephone" : 65,
    "Covered Bike Parking" : 18,
    "Sport" : 57,
    "Public WC" : 52,
    "P2" : 23,
    "Library Location" : 38,
    "Copy Machine" : 30,
    "Taxi Meeting Point" : 30,
    "Info Point" : 30,
    "Underground" : 30,
    "Sondersammlungen" : 30,
    "P4" : 30,
    "Computer Desks" : 30,
    "Study Area (Library)" : 30,
    "Telephone Zone" : 30,
    "Restaurant" : 30,
    "Search Terminal" : 30,
    "Surfstation" : 30,
    "Ramp Up" : 30,
    "Change Room" : 30,
    "Library Information" : 30,
    "Bookstore" : 30,
    "Entrance" : 30,
    "Delivery" : 30,
    "Barrier-free WC" : 30,
    "Self-service terminals" : 30,
    "Mens WC" : 30,
    "Women WC" : 30,
    "Infoterminal" : 30,
    "Play School" : 30,
    "Locker" : 30,
    "Scanner (Library)" : 30,
    "Front Office Web & New Media" : 30,
    "Search Terminal (Library)" : 30,
    "Sights" : 30,
    "Quiet Room" : 30,
    "Quiet room / First aid" : 30,
    "Grocery" : 30,
    "Bus" : 30,
    "Assembly point" : 30,
    "Entrance underground parking" : 30,
    "Computer Rooms" : 30,
    "Cafe/Snack" : 30,
    "P1" : 30,
    "Vending Machine" : 30,
    "Company medical officer" : 30,
    "Self-Checkout" : 30,
    "Bike" : 30,
    "Toilet" : 30,
    "Bank Machine" : 30,
    "Study Area" : 30,
    "ELSA WU" : 30,
    "Motor Bike Parking" : 30,
    "Taxi Stand" : 30,
    "Scanner" : 30

}

poi_cats_indrz = {
    1:"Access",
    2:"Education",
    3:"Facilities",
    4:"Public Infrastructure",
    5:"Safety & Security",
    6:"Parking",
    7:"Public Transport",
    8:"Library",
    9:"Food",
    10:"Shop",
    11:"Toilet",
    12:"Other",
    13:"Entrance",
    14:"Info Point",
    15:"Info Terminal",
    16:"Ramp Up",
    17:"Bike",
    18:"Bike Covered",
    19:"Delivery",
    20:"Entrance Underground Parking",
    21:"Motor Bike",
    22:"P1",
    23:"P2",
    24:"P3",
    25:"P4",
    26:"Bus",
    27:"Underground",
    28:"Taxi",
    29:"Taxi Meeting Point",
    30:"Front Office",
    31:"Front Office Web & New Media",
    32:"Study Area",
    33:"Surf Station",
    34:"Self Service Terminal",
    35:"Computer Room",
    37:"Information",
    38:"Library Location",
    39:"Quiet Room",
    40:"Scanner",
    41:"Search Terminal",
    42:"Self Checkout",
    43:"Study Area",
    44:"Computer Desks",
    45:"Telephone Zone",
    47:"Restaurant",
    48:"Vending Machine",
    49:"Cafe - Snack",
    50:"Bookstore",
    51:"Grocery",
    52:"Public WC",
    53:"Toilet",
    54:"Mens WC",
    55:"Womens WC",
    56:"Barrierfree WC",
    57:"Sport",
    58:"Sights",
    60:"Change Rooms",
    61:"Copy Machines",
    62:"Locker",
    63:"Bank Machine",
    64:"Company Medical Officer",
    65:"Emergency Telephone",
    66:"Quiet Room -  First Aid",
    67:"Meeting Point"

}

