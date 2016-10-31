      SELECT seq,
        id1 AS node,
        id2 AS edge,
          ST_Length(geom) AS cost,
           floor,
          network_type,
          ST_AsGeoJSON(geom) AS geoj
          FROM pgr_dijkstra('SELECT id, source, target,
                     total_cost:: DOUBLE PRECISION AS cost,
                     floor, network_type
                     FROM geodata.networklines_3857', 2186, 6154, FALSE, FALSE
          ) AS dij_route
          JOIN  geodata.networklines_3857 AS input_network
          ON dij_route.id2 = input_network.id ;
