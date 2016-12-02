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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
from geojson import loads, Feature, FeatureCollection

db_host = "gis-neu.wu.ac.at"
db_user = 'indrz-wu'
db_passwd = 'QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU'
db_database = "indrz-wu"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user, port=db_port,
                        password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

# define our start and end coordinates in EPSG:3857
# set start and end floor level as integer 0,1,2 for example
x_start_coord = 1826680.46582487
y_start_coord = 6142500.4902269
start_floor = 4

x_end_coord = 1826352.2863924
y_end_coord =  6142827.88037845
end_floor = 1


# find the start node id within 1 meter of the given coordinate
# select from correct floor level using 3D Z value
# our Z Value is the same as the floor number as an integer
# used as input in routing query start point
start_node_query = """
    SELECT id FROM geodata.networklines_3857_vertices_pgr AS p
    WHERE ST_DWithin(the_geom, ST_GeomFromText('POINT(%s %s)',3857), 1)
    AND ST_Z(the_geom) = %s;"""

# locate the end node id within 1 meter of the given coordinate
end_node_query = """
    SELECT id FROM geodata.networklines_3857_vertices_pgr AS p
    WHERE ST_DWithin(the_geom, ST_GeomFromText('POINT(%s %s)',3857), 1)
    AND ST_Z(the_geom) = %s;"""

# run our query and pass in the 3 variables to the query
# make sure the order of variables is the same as the
# order in your query
cur.execute(start_node_query, (x_start_coord, y_start_coord, start_floor))
start_node_id = int(cur.fetchone()[0])

# get the end node id as an integer
cur.execute(end_node_query, (x_end_coord, y_end_coord, end_floor))
end_node_id = int(cur.fetchone()[0])


# pgRouting query to return our list of segments representing
# our shortest path Dijkstra results as GeoJSON
# query returns the shortest path between our start and end nodes above
# in 3D traversing floor levels and passing in the layer value = floor

# routing_query = '''
#     SELECT seq, id1 AS node, id2 AS edge, ST_Length(geom) AS cost, floor,
#       network_type, ST_AsGeoJSON(geom) AS geoj
#       FROM pgr_dijkstra(
#         'SELECT id as id, source, target, st_length(geom) AS cost,
#          floor, network_type
#          FROM geodata.networklines_3857',
#         %s, %s, FALSE, FALSE
#       ) AS dij_route
#       JOIN  geodata.networklines_3857 AS input_network
#       ON dij_route.id2 = input_network.id ;
#   '''

routing_query = """
 SELECT
  seq, id, node, edge, ST_Length(geom) AS cost, floor, network_type, ST_AsGeoJSON(geom) AS geoj
  FROM pgr_dijkstra( 'SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857', 2424, 3728) AS dij_route

  JOIN geodata.networklines_3857 AS input_network
  ON dij_route.edge = input_network.id ;


"""


# run our shortest path query
cur.execute(routing_query)

# get entire query results to work with
route_segments = cur.fetchall()

# empty list to hold each segment for our GeoJSON output
route_result = []

# loop over each segment in the result route segments
# create the list of our new GeoJSON
for segment in route_segments:
    seg_cost = segment[4]     # cost value
    layer_level = segment[5]  # floor number
    seg_type = segment[6]
    geojs = segment[7]        # geojson coordinates
    geojs_geom = loads(geojs) # load string to geom
    geojs_feat = Feature(geometry=geojs_geom, properties={'floor': layer_level,
                                                          'cost': seg_cost,
                                                          'type_id': seg_type})
    route_result.append(geojs_feat)

# using the geojson module to create our GeoJSON Feature Collection
geojs_fc = FeatureCollection(route_result)

# define the output folder and GeoJSON file name
output_geojson_route = "ch08_indoor_3d_route.geojson"


# save geojson to a file in our geodata folder
def write_geojson():
    with open(output_geojson_route, "w") as geojs_out:
        geojs_out.write(json.dumps(geojs_fc))


# run the write function to actually create the GeoJSON file
write_geojson()

# clean up and close database curson and connection
cur.close()
conn.close()