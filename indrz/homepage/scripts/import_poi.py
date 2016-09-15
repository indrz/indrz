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
                    ST_MULTI(ST_TRANSFORM(poi.geom, 3857)) as geom, poi.aks_nummer
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

                        insert_state = """INSERT INTO django.poi_manager_poi (name, floor_num, fk_building_floor_id,
                                                      fk_campus_id, fk_building_id, fk_poi_category_id, geom, description)
                                    VALUES (\'{0}\', \'{1}\', {2}, {3},\'{4}\',{5},\'{6}\',\'{7}\'  )""".format(poi_name, floor_level_txt, m_floor_id_value,
                                                                               1, building_id, 12, m_geom, poi_descript)
                        print(insert_state)
                        cur2.execute(insert_state)
                        conn2.commit()

                print('done inserting on building id: ' + str(building_id))



# for floor in table_abrev:
#     import_poi(floor)

poi_name_field_values = {
    "Front Office" : 30,
    "Emergency telephone" : 65,
    "Covered Bike Parking" : 18,
    "Sport" : 57,
    "Public WC" : 52,
    "P2" : 23,
    "Library Location" : 38,
    "Copy Machine" : 61,
    "Taxi Meeting Point" : 29,
    "Info Point" : 14,
    "Underground" : 27,
    "Sondersammlungen" : 30,
    "P4" : 25,
    "Computer Desks" : 44,
    "Study Area (Library)" : 43,
    "Telephone Zone" : 45,
    "Restaurant" : 47,
    "Search Terminal" : 41,
    "Surfstation" : 33,
    "Ramp Up" : 16,
    "Change Room" : 60,
    "Library Information" : 37,
    "Bookstore" : 50,
    "Entrance" : 13,
    "Delivery" : 19,
    "Barrier-free WC" : 56,
    "Self-service terminals" : 34,
    "Mens WC" : 54,
    "Women WC" : 55,
    "Infoterminal" : 15,
    "Play School" : 30,
    "Locker" : 62,
    "Scanner (Library)" : 40,
    "Front Office Web & New Media" : 31,
    "Search Terminal (Library)" : 41,
    "Sights" : 58,
    "Quiet Room" : 39,
    "Quiet room / First aid" : 66,
    "Grocery" : 51,
    "Bus" : 26,
    "Assembly point" : 67,
    "Entrance underground parking" : 20,
    "Computer Rooms" : 35,
    "Cafe/Snack" : 49,
    "P1" : 22,
    "Vending Machine" : 48,
    "Company medical officer" : 64,
    "Self-Checkout" : 42,
    "Bike" : 17,
    "Toilet" : 53,
    "Bank Machine" : 63,
    "Study Area" : 32,
    "ELSA WU" : 30,
    "Motor Bike Parking" : 21,
    "Taxi Stand" : 29,
    "Scanner" : 40

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

open_pois = {
"": 68,
"AD Entrance A": 13,
"Aerobic Room": 68,
"AR/Portier optional": 68,
"Archiv/Drucker": 68,
"Aula": 68,
"Aula Stud Lounges": 68,
"Automaten": 48,
"Automaten Aufstellung/Verkauf": 48,
"Automatenaufstellung/Verkauf": 48,
"Bakery Anker": 49,
"Ball Sports Hall": 57,
"Berndorf Library for Business Languages": 68,
"Bibliothek (Info/Rückgabe)": 68,
"Bibliothek Ausleihe": 68,
"Buchbinderei": 68,
"Cafeteria": 49,
"Cafeteria-Anrichte": 49,
"Cafeteria/Buffet": 49,
"COMIDA y Luz": 68,
"COMIDA y Pan": 68,
"Communicative Study Area": 32,
"Copy and Scan": 40,
"Copy Room": 40,
"Copy/Kopierer": 40,
"D2 Entrance A": 13,
"D2 Entrance B": 13,
"D2 Entrance C": 13,
"D2 Entrance D": 13,
"D2 Entrance E": 13,
"D3 Entrance D": 13,
"D5 Entrance": 13,
"Drucker/Vervielfältigung": 40,
"Druckernische": 40,
"Druckerraum": 40,
"Dusche": 68,
"Dusche/Waschraum": 68,
"Eingangshalle Bibliothek": 68,
"Entrance OMV Library": 13,
"Fitness Center Lobby": 57,
"Fitness Room": 57,
"Front Office Business, Employment and Social Security Law": 30,
"Front Office Economics": 30,
"Front Office Finance, Accounting and Statistics": 30,
"Front Office Foreign Language Business Communication": 30,
"Front Office Global Business and Trade": 30,
"Front Office Information Systems and Operations": 30,
"Front Office International Office": 30,
"Front Office IT-Services": 30,
"Front Office Management": 30,
"Front Office Marketing": 30,
"Front Office ÖH": 30,
"Front Office Public Law and Tax Law": 30,
"Front Office Raiffeisen Language Resource Center": 30,
"Front Office Socioeconomics": 30,
"Front Office Strategy and Innovation": 30,
"Front Office WU Alumni Club": 30,
"Front Office WU Executive Academy": 30,
"Front Office ZBP": 30,
"HT Supermarkt": 51,
"Information": 14,
"Infoschalter": 14,
"Infoterminal AD 1": 15,
"Infoterminal AD 2": 15,
"Infoterminal D1 1": 15,
"Infoterminal D1 2": 15,
"Infoterminal D2 A 1": 15,
"Infoterminal D2 A 2": 15,
"Infoterminal D2 B 1": 15,
"Infoterminal D2 B 2": 15,
"Infoterminal D2 C 1": 15,
"Infoterminal D2 C 2": 15,
"Infoterminal D2 D 1": 15,
"Infoterminal D2 D 2": 15,
"Infoterminal D3 E 1": 15,
"Infoterminal D3 E 2": 15,
"Infoterminal D3 F 1": 15,
"Infoterminal D3 F 2": 15,
"Infoterminal D4 A 1": 15,
"Infoterminal D4 A 2": 15,
"Infoterminal D4 B 1": 15,
"Infoterminal D4 B 2": 15,
"Infoterminal D5 1": 15,
"Infoterminal D5 2": 15,
"Infoterminal EA 1": 15,
"Infoterminal EA 2": 15,
"Infoterminal LC 1": 15,
"Infoterminal LC 2": 15,
"Infoterminal TC 1": 15,
"Infoterminal TC 2": 15,
"infrastructure": 68,
"IT Support Center": 68,
"Journals": 68,
"Kommunikation/Pausenraum": 68,
"Kompaktmagazin Zeitschriften": 68,
"Kopier FO": 40,
"Kopierer/Archiv": 40,
"Kopierraum?": 40,
"Lehrbuchsammlung": 68,
"Lesebereich": 68,
"Lesebereich Mezanin": 68,
"Leseplätze": 68,
"Library": 37,
"Library Cafe & Roastery": 37,
"Library for Law": 37,
"Library for Social Sciences": 37,
"Loading Yard": 68,
"Lobby": 68,
"Lounge": 68,
"Meet up point": 67,
"Meeting Room": 67,
"Meetingraum/Besprechung": 67,
"Mensa": 47,
"Newspapers": 68,
"None": 68,
"Nykke": 68,
"Portier  D4": 14,
"Portier D3 AD": 14,
"Portier EA": 14,
"Poststelle": 14,
"Printer": 61,
"Ramp": 16,
"Reception Rectorate": 14,
"Recherche/Leseplätze": 41,
"Reference Collection": 68,
"Restaurant Brewery": 47,
"Ruheraum": 39,
"RVK Classification OG 05": 68,
"RVK Classification OG 06": 68,
"Selbststudienzone/Allg.Übungsr.": 43,
"Self Study Area": 43,
"Service Desk": 37,
"Shop 1/Verkaufsraum": 10,
"Shop 2/Verkaufsraum": 10,
"Sitting Area": 32,
"Sondersammlungen Kurt W Rothschild und Josef Steindl": 68,
"Spar Supermarkt": 51,
"Spez Bib. Fremdsprachen Erschl.": 68,
"Spez Bibliothek Fremdsprachen A": 68,
"Spez Bibliothek Fremdsprachen C": 68,
"Spez. Bib. Fremdspr./Research": 68,
"Studierendenbücherei": 50,
"Study Service Center (SSC)": 68,
"Surfstation (ByteBar)": 33,
"Telephone Booth": 45,
"Textbook Collection": 68,
"Tresen Cafe": 49,
"Trinkbrunnen": 68,
"Umkleide Cafe": 49,
"Veranstaltungsräume-Stuhllager": 68,
"Veranstaltungsräume - Aula": 68,
"Veranstaltungsräume - Festsaal1": 68,
"Veranstaltungsräume - Festsaal2": 68,
"Veranstaltungsräume - Foyer": 68,
"Veranstaltungsräume - Garderobe": 68,
"Veranstaltungsräume - Stuhllage": 68,
"VIP/Speisesaal": 47,
"Workstation": 35
}

# office_spaces = { "%D2.%" : 63, "%EA.%": 63, "%D3.%": 63, "%D4.%": 63, "%D5.%": 63,"%LC.%": 63,"%SC.%": 63, "%AD.%": 63, "%TC.%": 63, "%D1.%": 63}

building_ids = {'EA': 1, 'D5': 6, 'AD':5, 'LC': 2, 'D1': 7, 'D2': 10, 'D3': 4, 'D4': 3, 'SC': 9, 'TC': 8}

# conn2 = psycopg2.connect(host='gis-neu.wu.ac.at', user='indrz-wu', port='5432',
#                          password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
# cur2 = conn2.cursor()

def assign_space_type():

    for k, v in open_pois.items():

        # sel_poi_cats = """UPDATE django.buildings_buildingfloorspace set space_type_id = {1}
        #                               WHERE short_name = \'{0}\'""".format(k.replace("'", "''"), v)

        sel_poi_cats = """UPDATE django.poi_manager_poi set fk_poi_category_id = {0}
                                      WHERE name LIKE \'{1}\'""".format(v, k.replace("'", "''"))

        print(sel_poi_cats)
        cur2.execute(sel_poi_cats)
        conn2.commit()

assign_space_type()


def assign_space_type():

    for k, v in poi_name_field_values.items():

        # sel_poi_cats = """UPDATE django.buildings_buildingfloorspace set space_type_id = {1}
        #                               WHERE short_name = \'{0}\'""".format(k.replace("'", "''"), v)

        sel_poi_cats = """UPDATE django.poi_manager_poi set fk_poi_category_id = {0}
                                      WHERE name LIKE \'{1}\'""".format(v, k.replace("'", "''"))

        print(sel_poi_cats)
        cur2.execute(sel_poi_cats)
        conn2.commit()

# assign_space_type()