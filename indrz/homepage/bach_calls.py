# Create your views here.
# coding: utf-8

###################################
#  Bach API Calls
#
#
###################################

import json
import urllib2
import simplejson


def load_json(data, url):
    """

    :param data: the input data as json
    :param url: the bach api url call to webservice
    :return: wu api json reponse for search
    """
    data = simplejson.dumps(data)
    headers = {
        'Content-Type': 'application/json-rpc',
    }
    req = urllib2.Request(url, data, headers)
    resp = urllib2.urlopen(req)
    data = resp.read()

    if data is not None:
        data = simplejson.loads(data)
        if 'result' in data:
            return data['result']  # return only the values in the result item
        else:
            return data
    else:
        return None


# this method is a helper method to call the BACH API method search directory
def bach_search_directory(searchStr):
    """

    :param searchStr: a string search of employees or organization name
    :return: json of employees or organization info
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
        # un-comment when WU ready to activate personen and organization search
        # return None


# this method is a helper method to call the BACH API method get_room_by_pkbig
def bach_get_room_by_pk_big(big_pk):
    """

    :param big_pk: enter aks_Nummer as string
    :return: json room information
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus'

    data = {
        'id': '0815',
        'method': 'get_room_by_pkbig',
        'params': (big_pk,),
    }

    # return load_json(data,url)

    return None


def bach_get_employee_details(search_string):
    """

    :param search_string: enter string name of employee
    :return:  json employee details
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/personnel'
    data = {
        'id': '0815',
        'method': 'get_employee_details',
        'params': (6396, search_string),
    }
    # return load_json(data, url)
    return None


def bach_get_organization_details(org_key):
    """

    :param org_key: input string organization id  orgid
    :return: json search result
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/personnel/'

    data = {
        'id': '0815',
        'method': 'get_organization_details',
        'params': (org_key,),
    }

    return load_json(data, url)
    # return None


def bach_search_rooms(search_string):
    """

    :param search_string: enter name for room
    :return: json search result
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus/'

    data = {
        'id': '0815',
        'method': 'search_rooms',
        'params': (search_string,),
    }

    return load_json(data, url)
    # return None


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
    # return load_json(data, url)
    return None


def bach_get_search_eventseries(search_event_string):
    """

    :param event:enter string name of event, lehrveranstaltung
    :return: json result of event in dict head 'events'
    """
    url = 'https://bach.wu.ac.at/z/BachAPI/campus/'

    data = {
        'id': '0815',
        'method': 'search_eventseries',
        'params': (search_event_string,),
    }

    # return load_json(data, url)
    return None