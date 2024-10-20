DROP SCHEMA IF EXISTS projet CASCADE;
CREATE SCHEMA projet;

--------------------------------------------------------------
-- Point
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.point CASCADE ;
CREATE TABLE projet.point (
    id_point serial PRIMARY KEY,
    x int,
    y int
);


--------------------------------------------------------------
-- Table d'association entre polygone et point
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.association_polygone_point;

CREATE table projet.association_polygone_point (
    id_point integer references projet.point(id_point),
    id_polygone integer references projet.polygone(id_polygone),
    ordre serial
);


--------------------------------------------------------------
-- Types de Polygone
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.polygone CASCADE ;

CREATE TABLE projet.polygone (
    id_polygone sequence PRIMARY KEY
);


--------------------------------------------------------------
-- Table d'association entre composante connexe et polygone
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.association_connexe_polygone CASCADE;

CREATE TABLE projet.association_connexe_polygone (
	id_polygone integer REFERENCES tp.polygone(id_polygone),
    id_comp_connexe integer REFERENCES tp.comp_connexe(id_comp_connexe),
    ordre sequence
    creux boolean
);


--------------------------------------------------------------
-- Composante connexe
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.comp_connexe CASCADE;

CREATE TABLE projet.comp_connexe (
    id_comp_connexe integer PRIMARY KEY,
    id_attack integer REFERENCES tp.attack(id_attack) ON DELETE CASCADE,
    level integer,
    PRIMARY KEY (id_pokemon, id_attack)
);

