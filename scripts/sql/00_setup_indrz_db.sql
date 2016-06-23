CREATE ROLE "indrz-wu" LOGIN ENCRYPTED PASSWORD 'md539091991722381dcef6112d1b681b5d5'
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

ALTER ROLE "indrz-wu" SET search_path = django, geodata, public;

CREATE DATABASE indrz
  WITH OWNER = "indrz-pg"
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'German_Austria.1252'
       LC_CTYPE = 'German_Austria.1252'
       CONNECTION LIMIT = -1;

CREATE EXTENSION postgis SCHEMA public VERSION "2.2.1";

CREATE EXTENSION pgrouting
  SCHEMA public
  VERSION "2.1.0";


CREATE SCHEMA django AUTHORIZATION "indrz-wu";
CREATE SCHEMA geodata AUTHORIZATION "indrz-wu";


