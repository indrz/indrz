-- Function: public._pgr_pointtoid(geometry, double precision, text, integer)

-- DROP FUNCTION public._pgr_pointtoid(geometry, double precision, text, integer);

CREATE OR REPLACE FUNCTION public._pgr_pointtoid3dIndrz(
    point geometry,
    tolerance double precision,
    vertname text,
    srid integer
   )
  RETURNS bigint AS
$BODY$
DECLARE
    rec record;
    pid bigint;
    pnt geometry;

BEGIN
      --pnt := st_translate(st_force_3d(point), 0.0, 0.0, coalesce(zlev :: FLOAT, 0.0));
      pnt := ST_Force3D(point);

      EXECUTE
        'SELECT
          id,
          the_geom
        FROM
          ' || vertname || '
        WHERE
          ST_Expand(ST_GeomFromText(st_astext(' || quote_literal(pnt :: TEXT) || '),' || srid || '), ' || text(tolerance) || ') && the_geom AND
          ST_3DLength(ST_makeline(the_geom, ST_GeomFromText(st_astext(' || quote_literal(pnt :: TEXT) || '),' || srid ||
        '))) < ' || text(tolerance) || ' ORDER BY ST_3DLength(ST_makeline(the_geom, ST_GeomFromText(st_astext(' ||
        quote_literal(pnt :: TEXT) || '),' || srid ||
        '))) LIMIT 1'
    INTO rec;


--     EXECUTE 'SELECT ST_3DDistance(
--         the_geom,
--         ST_GeomFromText(ST_AsText('
--                 || quote_literal(point::text)
--                 || '),'
--             || srid ||')) AS d, id, the_geom
--     FROM '||_pgr_quote_ident(vertname)||'
--     WHERE ST_3DDWithin(
--         the_geom,
--         ST_GeomFromText(
--             ST_AsText(' || quote_literal(point::text) ||'),
--             ' || srid || '),' || tolerance||')
--     ORDER BY d
--     LIMIT 1'
--     INTO rec ;

    IF rec.id IS NOT NULL THEN
        pid := rec.id;
    ELSE
        execute 'INSERT INTO '||_pgr_quote_ident(vertname)||' (the_geom) VALUES ('||quote_literal(point::text)||')';
        pid := lastval();
END IF;

RETURN pid;

END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION public._pgr_pointtoid3dIndrz(geometry, double precision, text, integer,FLOAT)
  OWNER TO postgres;
