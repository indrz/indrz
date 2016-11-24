-- if not, go ahead and update
-- make sure tables dont exist

drop table if exists geodata.networklines_ug01;
drop table if exists geodata.networklines_e00;
drop table if exists geodata.networklines_e01;
drop table if exists geodata.networklines_e02;
drop table if exists geodata.networklines_e03;


-- convert to 3d coordinates with EPSG:3857
SELECT id, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_ug01
  FROM django.routing_networklinesug01;

SELECT id, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e00
  FROM django.routing_networklinese00;

SELECT id, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e01
  FROM django.routing_networklinese01;

SELECT id, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e02
  FROM django.routing_networklinese02;

SELECT id, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e03
  FROM django.routing_networklinese03;

-- fill the 3rd coordinate according to their floor number
UPDATE geodata.networklines_ug01 SET geom=ST_Translate(ST_Force_3Dz(geom),0,0,-1);
UPDATE geodata.networklines_e00 SET geom=ST_Translate(ST_Force_3Dz(geom),0,0,0);
UPDATE geodata.networklines_e01 SET geom=ST_Translate(ST_Force_3Dz(geom),0,0,1);
UPDATE geodata.networklines_e02 SET geom=ST_Translate(ST_Force_3Dz(geom),0,0,2);
UPDATE geodata.networklines_e03 SET geom=ST_Translate(ST_Force_3Dz(geom),0,0,3);

UPDATE geodata.networklines_ug01 SET length =ST_Length(geom);
UPDATE geodata.networklines_e00 SET length =ST_Length(geom);
UPDATE geodata.networklines_e01 SET length =ST_Length(geom);
UPDATE geodata.networklines_e02 SET length =ST_Length(geom);
UPDATE geodata.networklines_e03 SET length =ST_Length(geom);

-- no cost should be 0 or NULL/empty
UPDATE geodata.networklines_ug01 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e00 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e01 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e02 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e03 SET cost=1 WHERE cost=0 or cost IS NULL;

-- update unique ids id accordingly
UPDATE geodata.networklines_ug01 SET id=id+100000;
UPDATE geodata.networklines_e00 SET id=id+200000;
UPDATE geodata.networklines_e01 SET id=id+300000;
UPDATE geodata.networklines_e02 SET id=id+400000;
UPDATE geodata.networklines_e03 SET id=id+500000;

-- merge all networkline floors into a single table for routing
DROP TABLE IF EXISTS geodata.networklines_3857;
SELECT * INTO geodata.networklines_3857 FROM
(
  (SELECT id, geom, length, network_type, length*ug01.cost as total_cost,
   -1 as floor FROM geodata.networklines_ug01 ug01) UNION
  (SELECT id, geom, length, network_type, length*e0.cost as total_cost,
   0 as floor FROM geodata.networklines_e00 e0) UNION
(SELECT id, geom, length, network_type, length*e1.cost as total_cost,
   1 as floor FROM geodata.networklines_e01 e1) UNION
(SELECT id, geom, length, network_type, length*e2.cost as total_cost,
   2 as floor FROM geodata.networklines_e02 e2) UNION
  (SELECT id, geom, length, network_type, length*e3.cost as total_cost,
   3 as floor FROM geodata.networklines_e03 e3)

)
as foo ORDER BY id;

CREATE INDEX geom_gist_index
   ON geodata.networklines_3857 USING gist (geom);

CREATE INDEX id_idx
   ON geodata.networklines_3857 USING btree (id ASC NULLS LAST);

CREATE INDEX network_layer_idx
  ON geodata.networklines_3857
  USING hash
  (floor);

-- create populate geometry view with info
SELECT Populate_Geometry_Columns('geodata.networklines_3857'::regclass);

-- update stairs, ramps and elevators to match with the next layer
UPDATE geodata.networklines_3857 SET geom=ST_AddPoint(geom,
  ST_EndPoint(ST_Translate(geom,0,0,1)))
  WHERE network_type=1 OR network_type=2 OR network_type=7;
-- remove the second last point
UPDATE geodata.networklines_3857 SET geom=ST_RemovePoint(geom,ST_NPoints(geom) - 2)
  WHERE network_type=1 OR network_type=2 OR network_type=7;


-- add columns source and target
ALTER TABLE geodata.networklines_3857 add column source integer;
ALTER TABLE geodata.networklines_3857 add column target integer;
ALTER TABLE geodata.networklines_3857 OWNER TO "indrz-pg";

-- we dont need the temporary tables any more, delete them
DROP TABLE IF EXISTS geodata.networklines_ug01;
DROP TABLE IF EXISTS geodata.networklines_e00;
DROP TABLE IF EXISTS geodata.networklines_e01;
DROP TABLE IF EXISTS geodata.networklines_e02;
DROP TABLE IF EXISTS geodata.networklines_e03;

-- remove route nodes vertices table if exists
DROP TABLE IF EXISTS geodata.networklines_3857_vertices_pgr;
-- building routing network vertices (fills source and target columns in those new tables)
SELECT public.pgr_createTopology3dIndrz('geodata.networklines_3857', 0.0001, 'geom', 'id');


--ALTER TABLE geodata.networklines_3857_vertices_pgr OWNER TO "indrz-pg";