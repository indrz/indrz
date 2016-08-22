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
# along with th
# is program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json

url_base = "http://gis-neu.wu.ac.at:8080/geoserver290/rest/workspace/"
auth = ('mdiener', 'Gis2012mrdSnlw')

headers = {
    'Content-type': 'text/xml',
}


def create_workspace(name):
    data = '<workspace><name>' + name + '</name></workspace>'

    requests.post('http://gis-neu.wu.ac.at:8080/geoserver290/rest/workspaces', auth=auth, headers=headers, data=data)


def get_workspaces():
    r = requests.get('http://gis-neu.wu.ac.at:8080/geoserver290/rest/workspaces.json', auth=auth, headers=headers)

    res = json.loads(r.text)

    for space in res['workspaces']['workspace']:
        print(space['name'])

    print(type(res))

    print(r.text)


def get_layers():
    r = requests.get('http://gis-neu.wu.ac.at:8080/geoserver290/rest/layers.json', auth=auth, headers=headers)

    res = json.loads(r.text)
    print(r.text)
    for lyr in res['layers']['layer']:
        print(lyr)
    print(type(res))

    print(r.text)


get_layers()


def create_layer(new_feature_name):
    data = "<featureType><name>" + new_feature_name + "</name></featureType>"
    r = requests.post(url_base + 'indrz/datastores/indrz-wu/featuretypes', auth=auth, headers=headers, data=data)

    print(r.text)
