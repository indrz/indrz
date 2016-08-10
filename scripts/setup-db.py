#!/usr/bin/python
# -*- coding: utf-8 -*-

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import subprocess
import os


db_superuser = "postgres"
db_superuser_pwd = "air"


def local_con():
    db_name = "indrz-wu"
    dbowner_name = "indrz-wu"
    dbowner_pwd = "QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU"
    dbport = "5434"
    dbhost = "localhost"

# wu wien current old server db connection
def wu_old_con():
    db_name = "wuwien"
    dbowner_name = "wuwien"
    dbowner_pwd = "oi4jtoiwjfds"
    dbport = "5432"
    dbhost = "gis.wu.ac.at"


def wu_new_con():
    db_name = "indrz-wu"
    dbowner_name = "indrz-wu"
    dbowner_pwd = "QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU"
    dbport = "5432"
    dbhost = "gis-neu.wu.ac.at"

    
# dbhost = "localhost"
# dbhost = "gis.wu.ac.at"


def create_init_db(create_role=False):
    """
    create the initial role to own the db
    create the new db as the db super user assign owner to new role
    :return: new db with new owner
    """
    con = connect(dbname='postgres', user=db_superuser, host=dbhost, port=dbport, password=db_superuser_pwd)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    
    if create_role:
        cur.execute('CREATE ROLE \"{0}\" LOGIN ENCRYPTED PASSWORD \'{1}\''.format(dbowner_name, dbowner_pwd))
        print("creating role")
    
    cur.execute('''CREATE DATABASE \"{0}\" WITH OWNER = \'{1}\'
                    ENCODING = \'UTF8\' TEMPLATE=template0 CONNECTION LIMIT = -1;'''.format(db_name, dbowner_name))
    print("creating database")
    cur.close()
    con.close()


def setup_db(connection=local_con()):
    """
    create new db schemas, set role search path to use schemas automatically
    add extensions postgis and pgrouting to new db
    :return: new db schemas and extensions for indrz
    """
    # connect to new database and setup schemas and search path and extensions
    con2 = connect(dbname=db_name, user=db_superuser, host=dbhost, port=dbport, password=db_superuser_pwd)

    sql1 = 'CREATE SCHEMA django AUTHORIZATION \"{0}\"'.format(dbowner_name)
    sql2 = 'CREATE SCHEMA geodata AUTHORIZATION \"{0}\"'.format(dbowner_name)
    cur2 = con2.cursor()
    cur2.execute(sql1)
    print("creating schema django")
    cur2.execute(sql2)
    print("creating schema geodata")

    cur2.execute('ALTER ROLE \"{0}\" SET search_path = django, geodata, public'.format(dbowner_name))

    print("updating role to use new schemas")
    cur2.execute('CREATE EXTENSION postgis SCHEMA public VERSION "2.2.2"')
    print("creating extension postgis")
    cur2.execute('CREATE EXTENSION pgrouting SCHEMA public VERSION "2.2.0";')
    print("creating extension pgrouting")
    con2.commit()
    cur2.close()
    con2.close()
    
    
def backup_db():
    db_name = "wuwien"
    dbowner_name = "postgres"
    dbowner_pwd = "gpjeGwzF4uPd98xVfPLp"
    dbport = "5432"
    dbhost = "gis.wu.ac.at"
    
    outfile=r"c:\02_DEV\01_projects\02_indrz\gitlab_wu\scripts\campusgis-old.backup"
    
    # Windows users can uncomment these two lines if needed
    pg_dump = r"c:\Program Files\PostgreSQL\9.5\bin\pg_dump.exe"

    # view what geometry types are available in our OSM file
    subprocess.call([pg_dump, "--host", dbhost, "--port", dbport, "--username", dbowner_name, "--format", "c", "--verbose", "--file", outfile, db_name])
    

def dropdb():
    # pg_restore = r"c:\Program Files\PostgreSQL\9.5\bin\pg_restore.exe"
    dropdb = r"c:\Program Files\PostgreSQL\9.5\bin\dropdb.exe"
    subprocess.call([dropdb, '-h', dbhost, "-p", dbport, "-U", db_superuser, db_name])
    
    
def restore_db():
    restore_file = r"c:\02_DEV\01_projects\02_indrz\gitlab_wu\scripts\indrz-wu-server.backup"
    pg_restore = r"c:\Program Files\PostgreSQL\9.5\bin\pg_restore.exe"
    subprocess.call([pg_restore, '-h', dbhost, "-p", dbport, "-U", dbowner_name, "--dbname", db_name, "--verbose", restore_file])
    
    
# create_init_db()
# setup_db()

backup_db()


# dropdb()
# create_init_db()
# setup_db()

# restore_db()

