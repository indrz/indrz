
CREATE SCHEMA test AUTHORIZATION postgres;

DROP TABLE IF EXISTS test.edge_table_e00;
DROP TABLE IF EXISTS test.edge_table_e01;
CREATE TABLE test.edge_table_e00 (
    id serial PRIMARY KEY ,
    dir character varying,
    source BIGINT,
    target BIGINT,
    cost FLOAT,
    reverse_cost FLOAT,
    x1 FLOAT,
    y1 FLOAT,
    z1 FLOAT,
    x2 FLOAT,
    y2 FLOAT,
    z2 FLOAT,
    floor_num INT,
    way_type character varying,
    length FLOAT
);

SELECT AddGeometryColumn ('test','edge_table_e00','geom',3857,'LINESTRING',3);

CREATE TABLE test.edge_table_e01 (
    id serial PRIMARY KEY ,
    dir character varying,
    source BIGINT,
    target BIGINT,
    cost FLOAT,
    reverse_cost FLOAT,
    x1 FLOAT,
    y1 FLOAT,
    z1 FLOAT,
    x2 FLOAT,
    y2 FLOAT,
    z2 FLOAT,
    floor_num INT,
    way_type character varying,
    length FLOAT
);
SELECT AddGeometryColumn ('test','edge_table_e01','geom',3857,'LINESTRING',3);

INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,0,0,   2,1,0); --1
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES (-1, 1,  2,1,0,   3,1,0); --2
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES (-1, 1,  3,1,0,   4,1,0); --3
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,1,0,   2,2,0); --4
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1,-1,  3,1,0,   3,2,0); --5
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  0,2,0,   1,2,0); --6
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  1,2,0,   2,2,0); --7
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,2,0,   3,2,0); --8
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  3,2,0,   4,2,0); --9
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,2,0,   2,3,0); --10
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1,-1,  3,2,0,   3,3,0); --11
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1,-1,  2,3,0,   3,3,0); --12
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1,-1,  3,3,0,   4,3,0); --13
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,3,0,   2,4,0); --14
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  4,2,0,   4,3,0); --15
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  4,1,0,   4,2,0); --16
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  0.5,3.5,0,  1.9909999999999,3.5,0); --17
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  3.5,2.3,0,  3.5,4,0); --18
INSERT INTO test.edge_table_e00 (cost,reverse_cost,x1,y1,z1,x2,y2,z2, way_type) VALUES ( 1, 1,  0,2,0,   0,3,0, 'stairs');  -- 19 first floor
INSERT INTO test.edge_table_e01 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  0,3,1,   1,3,1);  -- 20 first floor
INSERT INTO test.edge_table_e01 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  1,3,1,   2,2,1);  -- 21 first floor
INSERT INTO test.edge_table_e01 (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,2,1,   1,1,1);  -- 22 first floor

UPDATE test.edge_table_e00 SET geom = ST_MakeLine(ST_SetSRID(ST_MakePoint(x1,y1,z1),3857),ST_SetSRID(ST_MakePoint(x2,y2,z2),3857)),
    dir = CASE WHEN (cost>0 and reverse_cost>0) THEN 'B'   -- both ways
           WHEN (cost>0 and reverse_cost<0) THEN 'FT'  -- direction of the LINESSTRING
           WHEN (cost<0 and reverse_cost>0) THEN 'TF'  -- reverse direction of the LINESTRING

           ELSE '' END,
    floor_num = CASE WHEN (z1=0 or z2=0) THEN 0 ELSE 0 END;  

UPDATE test.edge_table_e01 SET geom = ST_MakeLine(ST_SetSRID(ST_MakePoint(x1,y1,z1),3857),ST_SetSRID(ST_MakePoint(x2,y2,z2),3857)),
    dir = CASE WHEN (cost>0 and reverse_cost>0) THEN 'B'   -- both ways
           WHEN (cost>0 and reverse_cost<0) THEN 'FT'  -- direction of the LINESSTRING
           WHEN (cost<0 and reverse_cost>0) THEN 'TF'  -- reverse direction of the LINESTRING

           ELSE '' END,
    floor_num = CASE WHEN (z1=1 or z2=1) THEN 1 ELSE 0 END;
    
DROP TABLE IF EXISTS test.networklines_e00;
DROP TABLE IF EXISTS test.networklines_e01;
    
    
-- convert to 3d coordinates with EPSG:3857
SELECT id, ST_Force3D(ST_Force2D(st_geometryN(geom, 1))) AS geom,
  way_type, cost, reverse_cost, length, 0 AS source, 0 AS target
  INTO test.networklines_e00
  FROM test.edge_table_e00;
  
  -- convert to 3d coordinates with EPSG:3857
SELECT id, ST_Force3D(ST_Force2D(st_geometryN(geom, 1))) AS geom,
  way_type, cost, reverse_cost, length, 0 AS source, 0 AS target
  INTO test.networklines_e01
  FROM test.edge_table_e01;
  
UPDATE test.networklines_e00 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,0);
UPDATE test.networklines_e01 SET geom=ST_Translate(ST_Force3DZ(geom),0,0,1);

UPDATE test.networklines_e00 SET length =ST_Length(geom);
UPDATE test.networklines_e01 SET length =ST_Length(geom);
  
UPDATE test.networklines_e00 SET id=id+100000;
UPDATE test.networklines_e01 SET id=id+200000;

DROP TABLE IF EXISTS test.networklines_3857;

SELECT * INTO test.networklines_3857 FROM
    (
      (SELECT id, geom, length, way_type, length*e0.cost as cost, reverse_cost,
       0 as floor FROM test.networklines_e00 e0) UNION
    (SELECT id, geom, length, way_type, length*e1.cost as cost, reverse_cost,
       1 as floor FROM test.networklines_e01 e1)

    )
    as foo ORDER BY id;
    

-- create populate geometry view with info
SELECT Populate_Geometry_Columns('test.networklines_3857'::regclass);


UPDATE test.networklines_3857 SET geom=ST_AddPoint(geom,ST_EndPoint(ST_Translate(geom,0,0,1)))
  WHERE way_type='stairs';
-- remove the second last point
UPDATE test.networklines_3857 SET geom=ST_RemovePoint(geom,ST_NPoints(geom) - 2)
  WHERE way_type='stairs';
  
  -- add columns source and target
ALTER TABLE test.networklines_3857 add column source integer;
ALTER TABLE test.networklines_3857 add column target integer;
ALTER TABLE test.networklines_3857 OWNER TO "postgres";


DROP TABLE IF EXISTS test.networklines_e00;
DROP TABLE IF EXISTS test.networklines_e01;
DROP TABLE IF EXISTS test.networklines_3857_vertices_pgr;
SELECT pgr_createtopology3dIndrz('test.networklines_3857',0.0001, 'geom', 'id');

SELECT * FROM pgr_dijkstra(
    'SELECT id, source, target, cost, reverse_cost FROM test.networklines_3857',
    1, 20, FALSE
);

SELECT id, source, target, st_asewkt(geom) from test.networklines_3857 ORDER BY id;
