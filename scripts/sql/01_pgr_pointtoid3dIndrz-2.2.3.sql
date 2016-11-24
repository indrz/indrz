CREATE OR REPLACE FUNCTION public._pgr_pointtoid3dIndrz(
    point geometry,
    tolerance double precision,
    vertname text,
    srid integer)
  RETURNS bigint AS
$BODY$
DECLARE
    rec record;
    pid bigint;

BEGIN

    EXECUTE 'SELECT ST_3DDistance(
        the_geom,
        ST_GeomFromText(ST_AsText('
                || quote_literal(point::text)
                || '),'
            || srid ||')) AS d, id, the_geom
    FROM '||_pgr_quote_ident(vertname)||'
    WHERE ST_DWithin(
        the_geom,
        ST_GeomFromText(
            ST_AsText(' || quote_literal(point::text) ||'),
            ' || srid || '),' || tolerance||')
    ORDER BY d
    LIMIT 1' INTO rec ;
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
ALTER FUNCTION public._pgr_pointtoid3dIndrz(geometry, double precision, text, integer)
  OWNER TO postgres;
