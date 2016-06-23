#!/usr/bin/python
# -*- coding: utf-8 -*-

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

db_superuser = "postgres"
db_superuser_pwd = "somesecret"

db_name = "indrz"
dbowner_name = "indrz"
dbowner_pwd = "somesecret"
dbport = "5432"
dbhost = "localhost"


def create_init_db():
    """
    create the initial role to own the db
    create the new db as the db super user assign owner to new role
    :return: new db with new owner
    """
    con = connect(dbname='postgres', user=db_superuser, host=dbhost, port=dbport, password=db_superuser_pwd)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('CREATE ROLE \"{0}\" LOGIN ENCRYPTED PASSWORD \'{1}\''.format(dbowner_name, dbowner_pwd))
    print("creating role")
    cur.execute('''CREATE DATABASE \"{0}\" WITH OWNER = \'{1}\'
                    ENCODING = \'UTF8\' TEMPLATE=template0 CONNECTION LIMIT = -1;'''.format(db_name, dbowner_name))
    print("creating database")
    cur.close()
    con.close()


def setup_db():
    """
    create new db schemas, set role search path to use schemas automatically
    add extensions postgis and pgrouting to new db
    :return: new db schemas and extensions for indrz
    """
    # connect to new database and setup schemas and search path and extensions
    con2 = connect(dbname=db_name, user=db_superuser, host=dbhost, port=dbport, password=db_superuser_pwd)

    sql1 = 'CREATE SCHEMA django AUTHORIZATION "indrz-wu"'
    sql2 = 'CREATE SCHEMA geodata AUTHORIZATION "indrz-wu"'
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


create_init_db()
setup_db()
