#!/usr/bin/env python
# coding: utf-8



#import urllib2
import urllib
import csv
import json
import time
from math import ceil
import requests
from pprint import pprint
from functools import reduce


# # helper method to call request and print out result object

# from __builtin__ import unicode


def load_json(data_in, external_url):
    """

    :param data: the input data as json
    :param external_url: the bach api url call to webservice
    :return: wu api json reponse for search
    """
    data_res = json.dumps(data_in)
    external_api_endpoint_url = external_url

    json_header = {
        'Content-Type': 'application/json',
    }

    req = requests.post(external_api_endpoint_url, data=data_res, headers=json_header)
    pprint(req.json())
    response_data = req.json()

    if response_data is not None:
        if 'result' in response_data:
            return response_data['result']  # return only the values in the result item
        else:
            return response_data
    else:
        return None


def get_room_center(aks_nummer):
    url = 'http://localhost/wuwien_django/api/'
    data = {
        'id': 'labla',
        'method': 'getRoomCenter',
        'params': [{'searchString': (aks_nummer)}],
        'jsonrpc': '2.0'
    }
    data = json.dumps(data)
    print(data)

    json_headers = {
        'Content-Type': 'application/json',
    }

    req = requests.post(url, data=data, headers=json_headers)
    response_data = req.text


    if response_data is not None:

        if 'result' in response_data:
            return response_data['result']  # return only the values in the result item
        else:
            return response_data
    else:
        return None

pprint(get_room_center('001_10_EG01_311200'))

def test_route_terminal(ipTerminal):
    url = 'http://localhost:8000/terminal'
    data = {'id': 'labla', 'method': 'routeFromTerminal', 'params': [{'searchCriteria': ('123.40.45.12')}],
            'jsonrpc': '2.0'}

    test_req = {"method": "routeFromTerminal", "id": "labla",
                "params": [{"lat": 6142327.42710947, "lon": 1826614.23069183, "layer": 0,
                            "routeNodeAttributes": {"featureType":"point","building":"D2","external_id":"214","layer":"0","title":"D2.0.025 Workstation-Raum","type":"room/eg00","externalGraphic":"img/map_search_marker_h.png","aks_nummer":"001_30_EG01_010600","name_de":"D2.0.025 Workstation-Raum","name_en":"D2.0.025 Workstation Room","roomcode_value":"D2.0.025","orgid":"","frontoffice":"","entrance":"10280","entrance_name_en":"D2 Entrance C","entrance_name_de":"D2 Eingang C","category_de":"PC Raum","category_en":"PC room"},
                            "searchCriteria":{"type":"terminal"}}],
                "jsonrpc":"2.0"}


    request_data = {"method": "routeFromTerminal",
                    "id": "labla",
                    "params":
                        [{"lat": 6142345.36970451, "lon": 1826591.77149181, "layer": 0,
                          "routeNodeAttributes":
                              {"featureType": "point", "building": "D2",
                               "external_id": "216", "layer": "0", "title": "D2.0.039 Workstation-Raum Übungsraum",
                               "type": "room/eg00", "externalGraphic": "img/map_search_marker_j.png",
                               "aks_nummer": "001_30_EG01_010400", "name_de": "D2.0.039 Workstation-Raum Übungsraum",
                               "name_en": "D2.0.039 Workstation Room", "roomcode_value": "D2.0.039", "orgid": "",
                               "frontoffice": "", "entrance": "10280", "entrance_name_en": "D2 Entrance C",
                               "entrance_name_de": "D2 Eingang C", "category_de": "PC Raum", "category_en": "PC room"},
                          "searchCriteria": {"type": "terminal"}}],
                    "jsonrpc": "2.0"}
    data = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
    }

    r = requests.post("http://localhost:8000/api/", params=data)
    print(r.text)


# test_route_terminal("137.208.92.229")
# # print 'type: ' + str(type(data_pk_big)) + '  data_pk_big length: ' + str(len(data_pk_big))
# pprint.pprint(data_terminal)

### test webservice call get_room_center
# data_rooms = get_room_center('001_20_EG01_018700')
# pprint(data_rooms)


# this works and is tested
def bach_search_directory(searchStr):
    """

    :param searchStr: a string
    :return: json
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/directory'
    data = {
        'id': '0815',
        'method': 'search_directory',
        'params': (searchStr,),
    }

    # res is a list of dictionaries ie json
    res = load_json(data, url)
    filter_res = []

    # check that the show_directory: value is true
    # if true return to search if not hide
    if res is not None:
        for thing in res:
            if "show_directory" in thing:
                is_true = thing["show_directory"]
                if is_true:
                    filter_res.append(thing)
            else:
                return None

        return filter_res
    else:
        return None


#data_search_dir = bach_search_directory("IT-service")
#data_search_dir = bach_search_directory("Irene Fellner")
# data_search_dir = bach_search_directory("test")
#print 'type: ' + str(type(data_pk_big)) + '  data_pk_big length: ' + str(len(data_pk_big))
#pprint.pprint(data_search_dir)

# this method is a helper method to call the BACH API method get_room_by_pkbig
# this works and is tested
def bach_get_room_by_pk_big(big_pk):
    """

    :param big_pk:
    :return:
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus'

    data = {
        'id': '0815',
        'method': 'get_room_by_pkbig',
        'params': (big_pk,),
    }

    return load_json(data, url)


def bach_get_all_bookable_rooms():
    """

    :return: all rooms available in bach for booking as json in set Result
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus'

    data = {
        'id': '0815',
        'method': 'get_campus2013',
        'params': (),
    }
    # data = json.dumps(data)
    data = json.dumps(data)  # this will encode the data into json format
    headers = {
        'Content-Type': 'application/json-rpc',
    }

    req = urllib.request(url, data, headers)
    resp = urllib.request.urlopen(req)
    data = resp.read().encode('utf-8')
    decoded_json = json.loads(data, 'utf-8')  # this will decode json into strings
    # decoded_json = decoded_json['result']
    #### http://stackoverflow.com/questions/5838605/python-dictwriter-writing-utf-8-encoded-csv-files
    # D = {'name':u'马克','pinyin':u'mǎkè',u'test':1200}
    # print type(D)
    if 'result' in decoded_json:
        return decoded_json['result']
    else:
        return None


def bach_get_all_rooms():
    """

    :return: all rooms available in bach for booking as json in set Result
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus'

    data = {
        'id': '0815',
        'method': 'get_campus2013',
        'params': (),
    }
    return load_json(data, url)


# this works and is tested
def bach_get_employee_details(search_string):
    url = 'https://bach.wu.ac.at/z/BachAPI/personnel'
    data = {
        'id': '0815',
        'method': 'get_employee_details',
        'params': (6396, search_string),
    }

    res = load_json(data, url)

    if "show_directory" in res:
        print("yes key is here")
        is_true = res["show_directory"]
        print (is_true)
        if is_true:
            print ("value is TRUE go ahead and use it")
        else:
            print ("the value is FALSE to NOT use")
    else:
        print ("did not find key")

    return res


##### print to screen search employees #####
# data_employees = bach_get_employee_details("D")
# pprint.pprint(data_employees)


# this method is a helper method to call the BACH API method get_organization details
# this works and is tested
def bach_get_organization_details(org_key):
    """

    :param org_key:
    :return:
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/personnel/'

    data = {
        'id': '0815',
        'method': 'get_organization_details',
        'params': (org_key,),
    }

    res = load_json(data, url)

    if "show_directory" in res:
        print("yes key is here")
        is_true = res["show_directory"]
        print(is_true)

        if is_true:
            print("value is TRUE go ahead and use it")
        else:
            print("the value is FALSE to NOT use")
    else:
        print("did not find key")

    return res

# data_org_details = bach_get_organization_details("3944")
# pprint(data_org_details)

def bach_get_search_eventseries(search_event_string):
    """

    :param event:
    :return:
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus/'

    data = {
        'id': '0815',
        'method': 'search_eventseries',
        'params': (search_event_string,),
    }

    return load_json(data, url)


def bach_search_rooms(search_string):
    """

    :param search_string:
    :return:
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus/'

    data = {
        'id': '0815',
        'method': 'search_rooms',
        'params': (search_string,),
    }

    return load_json(data, url)


def export_to_csv(file_name, json_data):
    """

    :param file_name: enter file name includine extion like this  myfile.csv
    :param json_data:
    """
    D = json_data
    output_csv_file = open(file_name, 'wb')
    # f.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    w = csv.DictWriter(output_csv_file, sorted(D[0].keys()), delimiter='\t')
    w.writeheader()
    for each_value in D:
        # w.writerow({k: unicode(v).encode('utf-8') for k, v in
        w.writerow({k: v.encode('utf-8') for k, v in
                    each_value.items()})  # works !!! finaly #http://stackoverflow.com/questions/11884190/python-csv-unicode-ascii-codec-cant-encode-character-u-xf6-in-position-1-o

    output_csv_file.close()


def bach_get_headcount():
    """
    :return: json result of building study zone capacity and current head count'
    """

    url = 'https://bach.wu.ac.at/z/BachAPI/campus/headcount#'

    # python dictionary of json data
    test_json = {'buildings': [{'floors': [
        {'zones': [{'headcount': 250, 'capacity': 211, 'name': 'a'}], 'name': 'OG02'},
        {'zones': [{'headcount': 199, 'capacity': 400, 'name': 'a'}], 'name': 'OG03'},
        {'zones': [{'headcount': 200, 'capacity': 251, 'name': 'a'}, {'headcount': 6, 'capacity': 197, 'name': 'b'}],
         'name': 'OG04'},
        {'zones': [{'headcount': 55, 'capacity': 220, 'name': 'a'}, {'headcount': 67, 'capacity': 159, 'name': 'b'}],
         'name': 'OG05'}], 'name': 'LC'}, {'floors': [
        {'zones': [{'headcount': 4, 'capacity': 10, 'name': 'a'}], 'name': 'OG02'},
        {'zones': [{'headcount': 2, 'capacity': 10, 'name': 'a'}], 'name': 'OG03'},
        {'zones': [{'headcount': 5, 'capacity': 10, 'name': 'a'}, {'headcount': 9, 'capacity': 10, 'name': 'b'}],
         'name': 'OG04'},
        {'zones': [{'headcount': 1, 'capacity': 10, 'name': 'a'}, {'headcount': 7, 'capacity': 10, 'name': 'b'}],
         'name': 'OG05'}], 'name': 'EA'}], 'last_update': '2014-06-12T10:55:00'}

    # req = urllib2.Request(url)
    # opener = urllib2.build_opener()
    # f = opener.open(req)

    # wu studyzone capacity url data is a python dictionary {}
    # we need to first read it in as a string
    # then load it into a python dictionary type so we can work with it
    # to return json just use json.dump to pump out json from your dictionary

    # use json module to dump url to string object
    # jsond = json.dumps(f.read().decode('utf-8'))

    # use json module to create string object to work with from url
    # json_dict = json.loads(jsond)

    # json loader likes "" double quotes not single quotes to import into dict obj
    # fixit = json_dict.replace("'", "\"")

    # create dict object for us to work with 
    ### remove comment below to get live data and comment out 278 capacity_data
    # capacity_data = json.loads(fixit)
    # f.close()


    #######
    # test offline dict
    #######
    json_string = str(test_json)
    jsond2 = json.dumps(json_string)
    json_load = json.loads(jsond2)
    json_load_fix = json_load.replace("'", "\"")
    capacity_data = json.loads(json_load_fix)
    #######
    # end offline test
    #######

    valid_floors = ('UG01', 'EG00', 'OG01', 'OG02', 'OG03', 'OG04', 'OG05', 'OG06')
    valid_buildings = ('LC', 'EA', 'TC', 'D4', 'D3', 'D2', 'D5')
    valid_zone_names = ('a', 'b')
    zones = []
    headcount = 5.0
    capacity = 10.0
    zone_name = ''

    if 'buildings' in capacity_data:

        number_of_buildings = len(capacity_data['buildings'])

        if number_of_buildings > 0:

            # print capacity_data['buildings'][0]['floors'][0]['zones'][0]['headcount']

            # list of buildings
            buildings = capacity_data['buildings']
            for building in buildings:
                # print building
                building_name = building['name']
                # print building_name
                floors = building['floors']
                # loop through list of floors
                for floor in floors:
                    # print floor
                    zones = floor['zones']
                    floor_name = floor['name']
                    floor_number = floor_name[-1]

                    # print floor_name
                    # print zones
                    floor_rooms = 'wuwien:' + floor_name + '_rooms'
                    layer_studyzone = 'wuwien:' + floor_name + '_studyzone'
                    bbox = '1826287.67579913,6142131.83432293,1826932.875,6142846.30782982'

                    base_wms_url = 'http://gis.wu.ac.at/geoserver/wuwien/wms?service=WMS&version=1.3.0&request=GetMap&layers=' + layer_studyzone + \
                                   '&styles=&bbox=' + bbox + '&width=900&height=900&srs=EPSG:900913&format=image/png'
                    # print base_wms_url
                    # print len(zones)
                    # print zones[0]
                    # print len(zones)
                    num_zones = len(zones)
                    if num_zones == 1:
                        zone_a = zones[0]['name']
                        # print zone_a
                    else:
                        zone_b = zones[1]['name']
                        # print zone_b
                        zones_ab = str(zone_a) + ':' + '000066' + ';' + str(zone_b) + ':' + '000066'

                        print (zones_ab)

                    # capacity_url = base_wms_url + zone_hex

                    # print base_wms_url
                    # base_wms_url_d = base_wms_url + zone_name + ':' + hex_line_value
                    # print base_wms_url_d

                    # loop through nested list of zones
                    for zone in zones:
                        headcount = float(zone['headcount'])
                        capacity = float(zone['capacity'])
                        zone_name = zone['name']

                        if capacity == 0:
                            capacity = 1
                            headcount = 0
                            space_available = 2

                        space_available = int(ceil(float((headcount / capacity) * 100)))
                        # line 1 equals the hexvalue for 1% space used value
                        # line 2 equals the hexvalue for 2% space used value
                        # each line number represents the % value of space used
                        if space_available >= 100:
                            space_available = 100

                        # get line number using readlines and pass space_available -1
                        # -1 because it is the list index  value so 100 % is position [99]
                        hex_values_file = open("hexcolors.txt")
                        hex_line_obj = hex_values_file.readlines()[space_available - 1]
                        hex_line_value = hex_line_obj.strip()

                        # add the hex value to the zone dict if needed ?
                        # zone[u'hexcolor'] = hex_line_value
                        # zone[u'status'] = space_available
                        # print zone.fromkeys(['hexcolor','status'])

                        # print json.dumps(zone['hexcolor'])
                        # print zone
                        # print str(building_name) + ' ' + str(floor_name) \
                        # + ' ' + str(headcount) + ' ' + str(capacity) + ' ' + str(zone_name) \
                        # + ' ' + str(space_available) + '%' + ' ' + hex_line_value

                        # create_headcount_wms(floor_name, hex_line_value):
                        # output = {}
                        # print output['floorname': floor_name]

                        hex_values_file.close()
                        # print len(zones)
                        # zone_hex = []
                        # zone_hex.append('&env=' + zone_name + ':' + hex_line_value + ' ')
                        # print zone_hex

                        get_legend_graphic = 'http://gis.wu.ac.at/geoserver/wuwien/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=wuwien:og04_studyzone'
                        # print base_wms_url
                        # return wmsurl_space_available
        # no buildings in list
        else:
            return None
    # no elemement called buildings in dict
    else:
        return None


# bach_get_headcount()

def create_headcount_wms(floor_name='OG04', hexcolor='aaf60b'):
    floor_rooms = 'wuwien:' + str.lower(floor_name) + '_rooms'
    layer_studyzone = 'wuwien:' + floor_name + '_studyzone'
    # bbox is currently entire campus
    bbox = '1826287.67579913,6142131.83432293,1826932.875,6142846.30782982'
    base_wms_url = 'http://gis.wu.ac.at/geoserver/wuwien/wms?service=WMS&version=1.3.0&request=GetMap&layers=' + layer_studyzone + \
                   '&styles=&bbox=' + bbox + '&width=900&height=900&srs=EPSG:900913&format=image/png&env=color:' + hexcolor

    get_legend_graphic = 'http://gis.wu.ac.at/geoserver/wuwien/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=wuwien:og04_studyzone'
    print (base_wms_url)
    # return wmsurl_space_available


# create_headcount_wms('OG05','bbf70b')

# data_all_bookable_rooms = bach_get_all_bookable_rooms()
# fo = open("all_rooms.json", "wb")
# fo.write(str(data_all_bookable_rooms))
# fo.close()

# source http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
def getFromDict(dataDict, mapList):
    """
    dataDict: is a python dictionary with or without nested
    mapList: is a python list to specify the position in dictionary
    """
    mapList = ['buildings', ]

    return reduce(lambda d, k: d[k], mapList, dataDict)


def setInDict(dataDict, mapList, value):
    """
    dataDict: is a python dictionary with or without nested
    mapList: is a python list to specify the position in dictionary
    value: is the new value you assign to the key specified in mapList
    """
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value


###### export organization info to csv
# data_organizations = bach_get_organization_details("3510")  # 3628 Top Level WU org structure,  3792 departments, 3727 Finanz- und Rechnungswesen, 3510 Software Development, 3480 IT_Services, 3610 Finanzen und Infrastructure, 3610, 3513, 3944
# pprint.pprint(data_organizations)
# export_to_csv("demo_md2.csv", data_organizations)

# print 'type: ' + str(type(data_organizations)) + '  data_organizations length: ' + str(len(data_organizations))
# pprint.pprint(data_organizations)

##### export all rooms to csv #####
# data_all_bookable_rooms = bach_get_all_bookable_rooms()
# export_to_csv("all_bookable_rooms_new_2013-11-11_2125.csv", data_all_bookable_rooms)
# pprint.pprint(data_all_bookable_rooms[0]['buildingname'])

# try get all rooms in one call
# data_all_bookable_rooms = bach_get_all_rooms()
# pprint.pprint(data_all_bookable_rooms)

###### export organization info to csv
# data_organizations = bach_get_organization_details("3794")  # 3628 Top Level WU org structure,  3792 departments, 3727 Finanz- und Rechnungswesen, 3510 Software Development, 3480 IT_Services, 3610 Finanzen und Infrastructure, 3610, 3513, 3944
# pprint.pprint(data_organizations)

###### print to screen search_eventseries #####
# data_events = bach_get_search_eventseries('Current Issues on European and International Tax Law')
# pprint.pprint(data_events)

##### print to screen search _rooms #####
# data_events = bach_search_rooms('TC.3.03') #  sample search string 'erste'  or  'LC.4.076'
# pprint.pprint(data_events)

##### print to screen search employees #####
# data_employees = bach_get_employee_details('huber')
# pprint.pprint(data_employees)

##### print search rooms #####
# data_rooms = bach_search_directory('Fellner')
# pprint.pprint(data_rooms)

#### test bach_get_room_by_pk_big
# data_rooms = bach_get_room_by_pk_big('001_10_EG01_311200') # 001_10_EG01_311200
# pprint(data_rooms)




def test_call_autocomplete(searchString):
    items = []
    bachData_rooms = bach_search_rooms(searchString)

    print(type(searchString))  # type string
    # searchString = unicode(searchString, "utf-8")
    print(searchString)
    print(searchString.upper())
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

    print(items)

# python 2.7 code
# test_call_autocomplete(unicode('Hörsaal', 'utf-8'))

# test_call_autocomplete('Hörsaal')
# test_call_autocomplete('Erste')

start = time.time()
end = time.time()
print('total script time: ' + str(end - start))
