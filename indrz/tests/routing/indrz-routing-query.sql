SELECT
    seq,
    id1,
    id2,
      ST_Length(geom) AS cost,
       floor,
      network_type,
      ST_AsGeoJSON(geom) AS geoj
      FROM pgr_dijkstra('SELECT id, source, target,
                 cost:: DOUBLE PRECISION,
                 floor, network_type
                 FROM geodata.networklines_3857', 1863, 7008, FALSE,FALSE
      ) AS dij_route
      JOIN  geodata.networklines_3857 AS input_network
      ON dij_route.id2 = input_network.id ;


 SELECT
        seq, id, node, edge, ST_Length(geom) AS cost, floor, network_type, ST_AsGeoJSON(geom) AS geoj
          FROM 	pgr_dijkstra( 'SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857', 1863, 7008, FALSE, FALSE) AS dij_route
			
          JOIN  geodata.networklines_3857 AS input_network
          ON dij_route.edge = input_network.id ;
    


SELECT * FROM pgr_dijkstra(
    'SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857',
    2424, 1227
);

SELECT * FROM pgr_dijkstra(
    'SELECT id, source, target, cost, reverse_cost FROM geodata.networklines_3857',
    2424, 1227, FALSE, FALSE
);
