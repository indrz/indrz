--DROP TABLE indrz.buildings_organization cascade;

CREATE TABLE indrz.buildings_organization
(
  id serial PRIMARY KEY,
  street character varying(256),
  house_num character varying(10),
  postal_code character varying(8),
  municipality character varying(256),
  city character varying(256),
  country character varying(256),
  name character varying(256),
  description text,
  telephone character varying(32),
  email character varying(256),
  website character varying(256),
  geom geometry(Point,3857),
  owner character varying(128),
  legal_form character varying(128),
  num_buildings integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE indrz.buildings_organization
  OWNER TO wuwien;

  -- DROP TABLE indrz.buildings_campus;

CREATE TABLE indrz.buildings_campus
(
  id serial PRIMARY KEY,
  campus_name character varying(128),
  description character varying(256),
  geom geometry(MultiPolygon,3857),
  fk_organization_id integer NOT NULL,
  CONSTRAINT buildi_fk_organization_id_27ba423b_fk_buildings_organization_id FOREIGN KEY (fk_organization_id)
      REFERENCES indrz.buildings_organization (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE indrz.buildings_campus
  OWNER TO wuwien;


 -- DROP TABLE indrz.buildings_building;

CREATE TABLE indrz.buildings_building
(
  id serial PRIMARY KEY,
  street character varying(256),
  house_num character varying(10),
  postal_code character varying(8),
  municipality character varying(256),
  city character varying(256),
  country character varying(256),
  name character varying(256),
  description text,
  telephone character varying(32),
  email character varying(256),
  website character varying(256),
  geom geometry(Point,3857),
  building_name character varying(128),
  building_height numeric(10,2),
  fancy_name character varying(256),
  num_floors integer NOT NULL,
  facility_number integer,
  operation_hrs character varying(60),
  native_epsg integer,
  detail_description character varying(256),
  fk_campus_id integer,
  fk_organization_id integer NOT NULL,
  CONSTRAINT buildi_fk_organization_id_307aaaa2_fk_buildings_organization_id FOREIGN KEY (fk_organization_id)
      REFERENCES indrz.buildings_organization (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT buildings_building_fk_campus_id_963df2d6_fk_buildings_campus_id FOREIGN KEY (fk_campus_id)
      REFERENCES indrz.buildings_campus (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE indrz.buildings_building
  OWNER TO wuwien;

  CREATE TABLE indrz.buildings_buildingfloor
(
  id serial PRIMARY KEY,
  short_name character varying(150),
  long_name character varying(150),
  special_name character varying(150),
  vertical_order integer,
  base_elevation integer,
  floor_num integer,
  floor_height numeric(5,2),
  geom geometry(MultiPolygon,3857),
  fk_building_id integer NOT NULL,
  CONSTRAINT buildings_buil_fk_building_id_0d0e1dd3_fk_buildings_building_id FOREIGN KEY (fk_building_id)
      REFERENCES indrz.buildings_building (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE indrz.buildings_buildingfloor
  OWNER TO "wuwien";


CREATE TABLE indrz.buildings_ltaccesstype
(
  id serial PRIMARY KEY,
  code character varying(150),
  name character varying(256)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE indrz.buildings_ltaccesstype
  OWNER TO "wuwien";


CREATE TABLE indrz.buildings_ltspacetype
(
  id serial PRIMARY KEY,
  code character varying(150),
  name character varying(256)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE indrz.buildings_ltspacetype
  OWNER TO "wuwien";


  CREATE TABLE indrz.buildings_buildingfloorspace
(
  id serial PRIMARY KEY,
  short_name character varying(150),
  long_name character varying(150),
  area numeric(10,2),
  perimeter numeric(10,2),
  floor_num integer,
  geom geometry(MultiPolygon,3857),
  room_external_id character varying(150),
  room_number character varying(150),
  room_number_sign character varying(150),
  room_description character varying(150),
  capacity integer,
  tag text,
  fk_access_type_id integer,
  fk_building_id integer NOT NULL,
  fk_building_floor_id integer NOT NULL,
  space_type_id integer,
  CONSTRAINT bui_fk_building_floor_id_cb7f276a_fk_buildings_buildingfloor_id FOREIGN KEY (fk_building_floor_id)
      REFERENCES indrz.buildings_buildingfloor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT buildin_fk_access_type_id_013ffe5c_fk_buildings_ltaccesstype_id FOREIGN KEY (fk_access_type_id)
      REFERENCES indrz.buildings_ltaccesstype (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT buildings_bu_space_type_id_30f934cd_fk_buildings_ltspacetype_id FOREIGN KEY (space_type_id)
      REFERENCES indrz.buildings_ltspacetype (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT buildings_buil_fk_building_id_69db94af_fk_buildings_building_id FOREIGN KEY (fk_building_id)
      REFERENCES indrz.buildings_building (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE indrz.buildings_buildingfloorspace
  OWNER TO "wuwien";
