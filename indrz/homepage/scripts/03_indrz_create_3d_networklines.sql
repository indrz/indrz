-- if not, go ahead and update
-- make sure tables dont exist

drop table if exists geodata.networklines_ug01;
drop table if exists geodata.networklines_e00;
drop table if exists geodata.networklines_e01;
drop table if exists geodata.networklines_e02;
drop table if exists geodata.networklines_e03;
drop table if exists geodata.networklines_e04;
drop table if exists geodata.networklines_e05;
drop table if exists geodata.networklines_e06;


-- convert to 3d coordinates with EPSG:3857
SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_ug01
  FROM django.routing_networklinesug01;

SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e00
  FROM django.routing_networklinese00;

SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e01
  FROM django.routing_networklinese01;

SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e02
  FROM django.routing_networklinese02;

SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e03
  FROM django.routing_networklinese03;

SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e04
  FROM django.routing_networklinese04;

SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e05
  FROM django.routing_networklinese05;

SELECT id, ST_Force3D(ST_Transform(ST_Force2D(st_geometryN(geom, 1)),3857)) AS geom,
  network_type, cost::FLOAT, 0.0 AS reverse_cost, length, 0 AS source, 0 AS target
  INTO geodata.networklines_e06
  FROM django.routing_networklinese06;

-- fill the 3rd coordinate according to their floor number
UPDATE geodata.networklines_ug01 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,-1);
UPDATE geodata.networklines_e00 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,0);
UPDATE geodata.networklines_e01 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,1);
UPDATE geodata.networklines_e02 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,2);
UPDATE geodata.networklines_e03 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,3);
UPDATE geodata.networklines_e04 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,4);
UPDATE geodata.networklines_e05 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,5);
UPDATE geodata.networklines_e06 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,6);

UPDATE geodata.networklines_ug01 SET length =ST_Length(geom);
UPDATE geodata.networklines_e00 SET length =ST_Length(geom);
UPDATE geodata.networklines_e01 SET length =ST_Length(geom);
UPDATE geodata.networklines_e02 SET length =ST_Length(geom);
UPDATE geodata.networklines_e03 SET length =ST_Length(geom);
UPDATE geodata.networklines_e04 SET length =ST_Length(geom);
UPDATE geodata.networklines_e05 SET length =ST_Length(geom);
UPDATE geodata.networklines_e06 SET length =ST_Length(geom);

-- no cost should be 0 or NULL/empty
UPDATE geodata.networklines_ug01 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e00 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e01 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e02 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e03 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e04 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e05 SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.networklines_e06 SET cost=1 WHERE cost=0 or cost IS NULL;

-- update unique ids id accordingly
UPDATE geodata.networklines_ug01 SET id=id+100000;
UPDATE geodata.networklines_e00 SET id=id+200000;
UPDATE geodata.networklines_e01 SET id=id+300000;
UPDATE geodata.networklines_e02 SET id=id+400000;
UPDATE geodata.networklines_e03 SET id=id+500000;
UPDATE geodata.networklines_e04 SET id=id+600000;
UPDATE geodata.networklines_e05 SET id=id+700000;
UPDATE geodata.networklines_e06 SET id=id+800000;

-- merge all networkline floors into a single table for routing
DROP TABLE IF EXISTS geodata.networklines_3857;

SELECT * INTO geodata.networklines_3857 FROM
(
  (SELECT id, geom, length, network_type, length*ug01.cost as cost, reverse_cost::DOUBLE PRECISION,
   -1 as floor FROM geodata.networklines_ug01 ug01) UNION
  (SELECT id, geom, length, network_type, length*e0.cost as cost, reverse_cost::DOUBLE PRECISION,
   0 as floor FROM geodata.networklines_e00 e0) UNION
(SELECT id, geom, length, network_type, length*e1.cost as cost, reverse_cost::DOUBLE PRECISION,
   1 as floor FROM geodata.networklines_e01 e1) UNION
(SELECT id, geom, length, network_type, length*e2.cost as cost, reverse_cost::DOUBLE PRECISION,
   2 as floor FROM geodata.networklines_e02 e2) UNION
  (SELECT id, geom, length, network_type, length*e3.cost as cost, reverse_cost::DOUBLE PRECISION,
   3 as floor FROM geodata.networklines_e03 e3) UNION
  (SELECT id, geom, length, network_type, length*e4.cost as cost, reverse_cost::DOUBLE PRECISION,
   4 as floor FROM geodata.networklines_e04 e4) UNION
   (SELECT id, geom, length, network_type, length*e5.cost as cost, reverse_cost::DOUBLE PRECISION,
   5 as floor FROM geodata.networklines_e05 e5) UNION
  (SELECT id, geom, length, network_type, length*e6.cost as cost, reverse_cost::DOUBLE PRECISION,
   6 as floor FROM geodata.networklines_e06 e6)
)
as foo ORDER BY id;

UPDATE geodata.networklines_3857 set reverse_cost = cost;

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
  WHERE network_type=1 OR network_type=2 OR network_type=5;
-- remove the second last point
UPDATE geodata.networklines_3857 SET geom=ST_RemovePoint(geom,ST_NPoints(geom) - 2)
  WHERE network_type=1 OR network_type=2 OR network_type=5;


-- add columns source and target
ALTER TABLE geodata.networklines_3857 add column source integer;
ALTER TABLE geodata.networklines_3857 add column target integer;
ALTER TABLE geodata.networklines_3857 OWNER TO "indrz-wu";

-- we dont need the temporary tables any more, delete them
DROP TABLE IF EXISTS geodata.networklines_ug01;
DROP TABLE IF EXISTS geodata.networklines_e00;
DROP TABLE IF EXISTS geodata.networklines_e01;
DROP TABLE IF EXISTS geodata.networklines_e02;
DROP TABLE IF EXISTS geodata.networklines_e03;
DROP TABLE IF EXISTS geodata.networklines_e04;
DROP TABLE IF EXISTS geodata.networklines_e05;
DROP TABLE IF EXISTS geodata.networklines_e06;

-- remove route nodes vertices table if exists
DROP TABLE IF EXISTS geodata.networklines_3857_vertices_pgr;
-- building routing network vertices (fills source and target columns in those new tables)
SELECT public.pgr_createtopology3dIndrz('geodata.networklines_3857', 0.0001, 'geom', 'id', 'source', 'target', 'true', true);

--ALTER TABLE geodata.networklines_3857_vertices_pgr OWNER TO "indrz-wu";