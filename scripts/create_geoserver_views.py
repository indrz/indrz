
import psycopg2

db_superuser = "postgres"
db_superuser_pwd = "air"



db_name = "indrz-wu"
dbowner_name = "indrz-wu"
dbowner_pwd = "QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU"
dbport = "5434"
dbhost = "localhost"

conn1 = psycopg2.connect(host='localhost', user='postgres', port='5434', password='air', database='wu_old_db')
cur1 = conn1.cursor()

conn3 = psycopg2.connect(host='localhost', user='indrz-wu', port='5434', password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
cur3 = conn1.cursor()
# cur2.execute("select building, geom from geodata.og01_umriss")
# f = cur2.fetchall()
# print(f)

conn2 = psycopg2.connect(host='gis-neu.wu.ac.at', user='indrz-wu', port='5432', password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
cur2 = conn2.cursor()



pg_schema = ('geodata')
# table_abrev = ('ug01_', 'eg00_', 'og01_', 'og02_', 'og03_', 'og04_', 'og05_', 'og06_' )

table_abrev = ('ug01_', 'e00_', 'e01_', 'e02_', 'e03_', 'e04_', 'e05_', 'e06_' )

floor_values = ('poi', 'rooms', 'umriss', 'networklines', 'carto_lines', 'doors', 'furniture' )
other_tables = ('parking_garage', 'raumlist_buchungsys', 'temp_wu_personal_data' )
outdoor_tables = ('od_all_fill', 'od_all_polygons', 'od_baeume_linien', 'od_blindeleitlinie', 'od_fahrradstellplatz', 'od_familie_linie',
                  'od_orientierungselemente_linie', 'od_raucherzone', 'od_relax_area')
bibliothek_tables = ('bibliothek')

building_ids = {'EA': 1, 'D5': 6, 'AD':5, 'LC': 2, 'D1': 7, 'D2': 10, 'D3': 4, 'D4': 3, 'SC': 9, 'TC': 8}


def create_view(floor, table):

    floor_level_txt = floor[2:3]



    if table == 'carto_lines':
        q =  """

        CREATE OR REPLACE VIEW geodata.{0}{1} AS
         SELECT buildings_buildingfloorplanline.short_name,
            buildings_buildingfloorplanline.geom
           FROM django.buildings_buildingfloorplanline
          WHERE buildings_buildingfloorplanline.floor_num = {2} ;

        """.format(floor, table, floor_level_txt)

    if table == 'floor_footprint':
        q = """
            CREATE OR REPLACE VIEW geodata.{0}{1} AS
             SELECT buildings_buildingfloor.short_name,
                buildings_buildingfloor.geom
               FROM django.buildings_buildingfloor
              WHERE buildings_buildingfloor.floor_num = {2};

        """.format(floor, table, floor_level_txt)

    if table == 'space_polys':
        q = """
            drop view geodata.{0}{1};
            CREATE OR REPLACE VIEW geodata.{0}{1} AS
             SELECT buildings_buildingfloorspace.id,
             buildings_buildingfloorspace.short_name,
             buildings_buildingfloorspace.long_name,
             buildings_buildingfloorspace.room_code,
                buildings_buildingfloorspace.space_type_id,
                buildings_buildingfloorspace.geom
               FROM django.buildings_buildingfloorspace
              WHERE buildings_buildingfloorspace.floor_num = {2} ;
        """.format(floor, table, floor_level_txt)

    print('floor is now: ' + floor_level_txt)
    print(q)

    cur3.execute(q)
    conn3.commit()



views = ('carto_lines', 'floor_footprint', 'space_polys')


for floor in table_abrev:

    for space in views:

        create_view(floor, space)
