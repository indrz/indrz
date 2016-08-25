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

url_base = "http://gis-neu.wu.ac.at:8080/geoserver290/rest/"
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
    """
    A layer is a published feature
    :return:
    """
    r = requests.get('http://gis-neu.wu.ac.at:8080/geoserver290/rest/layers.json', auth=auth, headers=headers)

    res = json.loads(r.text)
    print(r.text)
    for lyr in res['layers']['layer']:
        print(lyr)
    print(type(res))

    print(r.text)


def create_layer(new_feature_name):
    # curl - v - u
    # admin:geoserver - XPOST - H
    # "Content-type: text/xml"
    # -drver / rest / workspaces / acme / datastores / nyc / featuretypes
    # "<featureType><name>buildings</name></featureType>"
    # http: // localhost:8080 / geose
    """

    :param new_feature_name:
    :return:
    """

    native_srs =    """
      <nativeCRS class="projected">PROJCS[&quot;WGS 84 / Pseudo-Mercator&quot;,
      GEOGCS[&quot;WGS 84&quot;,
        DATUM[&quot;World Geodetic System 1984&quot;,
          SPHEROID[&quot;WGS 84&quot;, 6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],
          AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],
        PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],
        UNIT[&quot;degree&quot;, 0.017453292519943295],
        AXIS[&quot;Geodetic longitude&quot;, EAST],
        AXIS[&quot;Geodetic latitude&quot;, NORTH],
        AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]],
      PROJECTION[&quot;Popular Visualisation Pseudo Mercator&quot;, AUTHORITY[&quot;EPSG&quot;,&quot;1024&quot;]],
      PARAMETER[&quot;semi_minor&quot;, 6378137.0],
      PARAMETER[&quot;latitude_of_origin&quot;, 0.0],
      PARAMETER[&quot;central_meridian&quot;, 0.0],
      PARAMETER[&quot;scale_factor&quot;, 1.0],
      PARAMETER[&quot;false_easting&quot;, 0.0],
      PARAMETER[&quot;false_northing&quot;, 0.0],
      UNIT[&quot;m&quot;, 1.0],
      AXIS[&quot;Easting&quot;, EAST],
      AXIS[&quot;Northing&quot;, NORTH],
      AUTHORITY[&quot;EPSG&quot;,&quot;3857&quot;]]</nativeCRS>

    """
    data = "<featureType><name>" + new_feature_name + "</name>" + native_srs + "<srs>EPSG:3857</srs><projectionPolicy>FORCE_DECLARED</projectionPolicy><enabled>true</enabled></featureType>"
    r = requests.post(url_base + 'workspaces/indrz/datastores/indrz-wu/featuretypes', auth=auth, headers=headers, data=data)
    # print(r.raise_for_status())
    print(r.content)
    print(r.reason)
    print(r.status_code)
    print(r.text)

levels_abrev = ('ug01_', 'e00_', 'e01_', 'e02_', 'e03_', 'e04_', 'e05_', 'e06_' )
views = ('carto_lines', 'floor_footprint', 'space_polys')


for level in levels_abrev:
    opt = '<nativeName>{0}space_polys</nativeName>'.format(level)
    curlevel = '{0}space_anno'.format(level)
    print(curlevel, opt)

    create_layer(curlevel)
