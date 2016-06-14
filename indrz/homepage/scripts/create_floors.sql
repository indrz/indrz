INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 1
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'EA';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 2
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'D5';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 3
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'AD';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 4
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'D3';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 5
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'D4';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 6
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'LC';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 7
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'D1';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 8
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'TC';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 9
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'D2';

INSERT INTO indrz.buildings_buildingfloor (geom, short_name, floor_num, fk_building_id)
SELECT st_transform(geom, 3857) as geom, building, 0, 10
FROM geodata.eg00_umriss
WHERE geodata.eg00_umriss.building = 'SC';