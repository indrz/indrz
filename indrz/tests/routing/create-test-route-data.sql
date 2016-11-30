DROP TABLE IF EXISTS test.edge_table;

CREATE TABLE test.edge_table (
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
    the_geom geometry
);



INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,0,0,   2,1,0); --1
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES (-1, 1,  2,1,0,   3,1,0); --2
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES (-1, 1,  3,1,0,   4,1,0); --3
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,1,0,   2,2,0); --4
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1,-1,  3,1,0,   3,2,0); --5
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  0,2,0,   1,2,0); --6
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  1,2,0,   2,2,0); --7
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,2,0,   3,2,0); --8
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  3,2,0,   4,2,0); --9
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,2,0,   2,3,0); --10
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1,-1,  3,2,0,   3,3,0); --11
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1,-1,  2,3,0,   3,3,0); --12
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1,-1,  3,3,0,   4,3,0); --13
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,3,0,   2,4,0); --14
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  4,2,0,   4,3,0); --15
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  4,1,0,   4,2,0); --16
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  0.5,3.5,0,  1.9909999999999,3.5,0); --17
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  3.5,2.3,0,  3.5,4,0); --18
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  0,2,0,   0,3,10);  -- 19 first floor
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  0,3,10,   1,3,10);  -- 20 first floor
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  1,3,10,   2,2,10);  -- 21 first floor
INSERT INTO test.edge_table (cost,reverse_cost,x1,y1,z1,x2,y2,z2) VALUES ( 1, 1,  2,2,10,   1,1,10);  -- 22 first floor



UPDATE test.edge_table SET the_geom = ST_MakeLine(ST_MakePoint(x1,y1,z1),ST_MakePoint(x2,y2,z2)),
    dir = CASE WHEN (cost>0 and reverse_cost>0) THEN 'B'   -- both ways
           WHEN (cost>0 and reverse_cost<0) THEN 'FT'  -- direction of the LINESSTRING
           WHEN (cost<0 and reverse_cost>0) THEN 'TF'  -- reverse direction of the LINESTRING

           ELSE '' END,
    floor_num = CASE WHEN (z1=1 or z2=1) THEN 1 ELSE 0 END;                                -- unknown

DROP TABLE IF EXISTS test.edge_table_vertices_pgr;
SELECT pgr_createtopology3dIndrz('test.edge_table',0.0001);

SELECT * FROM pgr_dijkstra(
    'SELECT id, source, target, cost, reverse_cost FROM test.edge_table',
    1, 20, FALSE
);