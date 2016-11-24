import os
import os.path
import psycopg2
# Database Connection Info
db_host = "localhost"
db_user = "indrz-pg"
db_passwd = "dm1vBJxpr70kkZO1udBY"
db_database = "indrz"
db_port = "5432"

conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)
cur = conn.cursor()

floors = ["ug01", "e00", "e01", "e02", "e03", "e04", "e05", "e06"]
extension_name = "routing_networklines"
level = None

def cleanup():
    for floor in floors:
        cur.execute("""drop table if exists geodata.networklines_{0}""".format(floor))


def create_3D_networklines(floors):
    for floor in floors:
        sql = """SELECT id, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(geom, 1)),3857)) AS geom,
          network_type, cost, length, 0 AS source, 0 AS target
          INTO geodata.networklines_{0}
          FROM django.routing_networklines{0}""".format(floor)
        print(floor)
        cur.execute(sql)
        conn.commit()

#create_3D_networklines()

def assign_z_elevation():
    for floor in floors:
        if floor == "ug01":
            level = -1
        elif floor == "e00":
            level = 0
        if floor == "e01":
            level = 1
        elif floor == "e02":
            level = 2
        elif floor == "e03":
            level = 3

        sql_update_3dz ="""UPDATE geodata.networklines_{0}
            SET geom=ST_Translate(ST_Force_3Dz(geom),0,0,{1}); """.format(floor, level)
        print(level)
        print(floor)
        cur.execute(sql_update_3dz)

        #cur.execute("""UPDATE geodata.networklines_{0} SET length =ST_Length(geom)""".format(floor))

        #cur.execute("""UPDATE geodata.networklines_{0} SET cost=1 WHERE cost=0 or cost IS NULL; """.format(floor))

        #cur.execute("""UPDATE geodata.networklines_{0} SET id=id+{1};""".format(floor,level*10000))
        conn.commit()

assign_z_elevation()

def merge_final_networklines():
    """

    :return:
    """

    sql = """
            -- merge all networkline floors into a single table for routing
    DROP TABLE IF EXISTS geodata.networklines_3857;
    SELECT * INTO geodata.networklines_3857 FROM
    (
    (SELECT id, geom, length, network_type, length*o1.cost as total_cost,
       1 as layer FROM geodata.networklines_e01 o1) UNION
    (SELECT id, geom, length, network_type, length*o2.cost as total_cost,
       2 as layer FROM geodata.routing_networklinese02 o2))
    as foo ORDER BY id;

    CREATE INDEX geom_gist_index
       ON geodata.networklines_3857 USING gist (geom);

    CREATE INDEX id_idx
       ON geodata.networklines_3857 USING btree (id ASC NULLS LAST);

    CREATE INDEX network_layer_idx
      ON geodata.networklines_3857
      USING hash
      (layer);

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
    ALTER TABLE geodata.networklines_3857 OWNER TO postgres;

    -- we dont need the temporary tables any more, delete them
    DROP TABLE IF EXISTS geodata.networklines_e01;
    DROP TABLE IF EXISTS geodata.routing_networklinese02;

    -- remove route nodes vertices table if exists
    DROP TABLE IF EXISTS geodata.networklines_3857_vertices_pgr;
    -- building routing network vertices (fills source and target columns in those new tables)
    SELECT public.pgr_createTopology3d('geodata.networklines_3857', 0.0001, 'geom', 'id');
        """

    cur.execute(sql)
