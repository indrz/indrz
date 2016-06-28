#!/bin/python
# coding: utf-8
import psycopg2
import time

# do a timestamp for being able to track execution time (if you want)
startscript = time.time()  # we will use this later

def create_db_conn():
    # Database Connection Info
    #db_host = "137.208.3.187"
    db_host = "localhost"
    #db_user = "indrz-wu"
    db_user = "postgres"
    db_passwd = "air"
    #db_passwd = "oi4jtoiwjfds"
    db_database = "wu_old_db"
    db_port = "5434"
    # get a connection handle to Postgresql queries
    conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)

    return conn


# list of the floors to update
# floor_list = ('ug01_poi', 'eg00_poi', 'og01_poi', 'og02_poi', 'og03_poi', 'og04_poi', 'og05_poi', 'og06_poi' )
pg_schema = ('geodata')
floor_n = ('ug01_', 'eg00_', 'og01_', 'og02_', 'og03_', 'og04_', 'og05_', 'og06_' )
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

conn2 = create_db_conn()
cur2 = conn2.cursor()
cur2.execute("select building, geom from geodata.og01_umriss")
f = cur2.fetchall()
# print(f)

conn3 = psycopg2.connect(host='localhost', user='indrz-wu', port='5434', password='air', database='indrz-wu')
cur3 = conn3.cursor()


##  STARAT IMPORT FLOORSs
def import_building_floors(floor_level):
    for k,v in building_ids.items():
        # k is Building short name
        # v is Builing id as integer
        if k:
            print(k,v)
            sel_buildings_floor = "SELECT building, floor, st_transform(geom, 3857) FROM geodata.{0}umriss WHERE building = \'{1}\'".format(floor_level, k)
            print(sel_buildings_floor)
            cur2.execute(sel_buildings_floor)
            res = cur2.fetchall()

            if res:
                floor_int = int(res[0][1])
                print(res)
                print(sel_buildings_floor)
                floor_label = floor_level.upper()[:2] + " " + floor_level[3:4] # og01_
                print(floor_label)
                print("building id is: " + str(v))

                insert_state = """INSERT INTO django.buildings_buildingfloor (short_name, fk_building_id, floor_num,geom)
                            VALUES (\'{0}\', {1}, {2}, \'{3}\' )""".format(floor_label, v, floor_int, res[0][2])
                # cur3.execute(insert_state)
                # conn3.commit()
                #print(insert_state)
                #print("DONE inserting for building: " + floor_level)

# for floor in floor_n:
#     if floor is not "eg00_":
#         import_building_floors(floor)

##    END IMPORT FLOORS

def import_floor_spaces(floor_abr):
    """

    :param floor_abr: floor abreviation og02_  for example
    :return:
    """
    for k,v in building_ids.items():
        if k:
            sel_spaces = """SELECT room_name, room_number, building, floor, description, aks_nummer, roomname_de,
             fancyname_de, category_de, roomcode, entrance_poi_id FROM geodata.{0}rooms as R, geodata.{0}umriss as U
             WHERE st_within(R.geom, U.geom)""".format(floor_abr)

            sel_spaces_new = """
             SELECT r.room_name, r.room_number, r.building, r.floor, r.description, r.aks_nummer,
              r. roomname_de,r.fancyname_de, r.category_de, r.roomcode, r.entrance_poi_id
           FROM geodata.og01_rooms as r, geodata.og01_umriss as U
           where st_within(r.geom,u.geom)
           AND u.building='EA'
            """

            cur2.execute(sel_spaces)
            res = cur2.fetchall()
            floor_level_txt = floor_abr[3:4]
            print( len(res))
            print(res)
            if res is not None or res == "":
                m_room_types = res[0][0]
                # print("room_name is : " + str(m_short_name))
                m_room_number = res[0][1]
                # print("room number is : " +  str(m_room_number))
                m_building = res[0][2]
                # print("room building is : " + str(m_building))
                m_floor = res[0][3]
                # print("floor is : " + str(m_floor))
                m_aks = res[0][5]
                # print("aks number is : " +  str(m_aks))
                m_roomname_de = res[0][6]

                m_fancyname_de = res[0][7]
                m_catname_de = res[0][8]
                m_roomcode = res[0][9]
                m_poi_entrance_id = res[0][10]
                # m_geom = res[0][11]
                #
                # sel_get_building_id = """SELECT id from django.buildings_buildingfloor as P WHERE ST_within({0},P.geom)""".format(m_geom)
                # cur3.execute(sel_get_building_id)
                # res_building_id = cur3.fetchall()


                sel_building_floor_id = """SELECT id, floor_num, fk_building_id from django.buildings_buildingfloor
                          WHERE floor_num = {0} and fk_building_id = {1}""".format(floor_level_txt, v)
                # print(sel_building_floor_id)

                cur3.execute(sel_building_floor_id)
                res_floor_id = cur3.fetchall()
                # print(res_floor_id)

                if res_floor_id:
                    # print(res_floor_id)
                    m_floor_id_value = res_floor_id[0][0]
                    # print("FLOOR ID : " + str(m_floor_id_value))
                    if m_floor_id_value > 79:
                        print("problem houston")


                # print("fancyname is : " +  str(m_fancyname_de))
                # print(len(res))

                # print(k)
                # print(sel_spaces)
                insert_state = """INSERT INTO django.buildings_buildingfloorspace (short_name, long_name, floor_num,
                    room_external_id, room_number, room_number_sign, room_description, fk_building_id,
                    fk_building_floor_id, space_type_id, roomcode, geom)
                            VALUES (\'{0}\', '\{1}\', {2}, \'{3}\',\'{4}\', \'{5}\',\'{6}\',
                            {7},{8},{9},\'{10}\',\'{11}\'  )""".format(m_fancyname_de, m_catname_de, m_floor, m_aks,
                                                      m_room_number, m_roomname_de, m_room_types, v, m_floor_id_value, 94, m_roomcode, "geom" )
                # cur3.execute(insert_state)
                # conn3.commit()
                # print(insert_state)


for floor in floor_n:
    import_floor_spaces(floor)



# def assign_space_type(floor_level):
#     for k,v in building_ids.items():
#         if k:


conn3.close()
conn2.close()
# list of database field names that we want to update
# you can only update one field at one time
# possible field name you can use 'name'
# possible field name you can use 'cat_main'
# possible field name you can use 'cat_sub'
# possible field name you can use 'description'
# possible field name you can use 'name_en'
# possible field name you can use 'cat_main_en'
# possible field name you can use 'cat_sub_en'
# possible field name you can use 'description_en'
# possible field name you can use 'sort_order'

# here are your variables to change for updating the pois
update_field_name = 'building' #enter the name of the field you wish to update
#old_value = u"Essen und Trinken" # enter the old database values you want to change
new_value = u"TC" # enter the NEW database values you want
where_claus = 'building'
where_value = 'D1 TC'

# here you must change the
def gen_datalist(data_type=0):
    """
    pass in the position
    :param data_type:
    :return:
    """
    poi_list = []
    for floor in floor_n:
        poi_list.append('geodata.' + floor + floor_values[data_type])
    return poi_list

def union_floor_data(data_list):
    merged_data = [] # data for all floors
    for table_name in data_list:
        term = "WC"
        sql_q = "select * from {0}"
        conn = create_db_conn()
        cur = conn.cursor()
        cur.execute(sql_q.format(table_name,), dict(like='%' + term + '%'))
        all_values = cur.fetchall()
        merged_data.append(all_values)

    return merged_data

# poi_list = gen_datalist(0)
# room_list = gen_datalist(1)
# umriss_list = gen_datalist(2)
# networklines_list = gen_datalist(3)
# carto_list = gen_datalist(4)
# doors_list = gen_datalist(5)
# furniture_list = gen_datalist(6)

# print(poi_list)
# print(room_list)
# term="WC"
# sql= "select room_name from geodata.og01_rooms where room_name LIKE %(like)s ESCAPE '='"
# cur.execute(sql, dict(like= '%'+term+'%'))

#cur.execute('select room_name from geodata.og01_rooms where room_name LIKE %(like)s'WC%';')
# conn2 = create_db_conn()
# cur2 = conn2.cursor()
# cur2.execute('select room_name from geodata.eg00_rooms')
# x = cur2.fetchall()
# print(x)

# for value in x:
#     first_val = value[0]
#     print(first_val)
#     if first_val is not None:
#         print(first_val)
# print (x)
# cols_names = [col_name[0] for col_name in cur2.description]
#
# cur2.close()
# conn2.close()
# print(cols_names)
# print(fx)


# if room_name value = x:
    # then set room type = foo:
# elif room_name value = y:
    # then set room _type = kaa

# def map_cols():
    # r = map(func, seq)





# for poi in poi_list:
#     cur.execute("UPDATE geodata."+poi+" SET "+update_field_name+" = %s WHERE "+where_claus+" = %s", (new_value, where_value,))

# conn.commit()
# cur.close()
# conn.close()

endscript = time.time()
endtime = endscript - startscript
print ('script run in ' + str(endscript - startscript) + ' seconds or ' + '\n'
       + str((endscript - startscript)*1000) + ' miliseconds')