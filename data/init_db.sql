DROP SCHEMA IF EXISTS projet CASCADE;

CREATE SCHEMA projet;

--------------------------------------------------------------
-- Zone
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.zone_geo CASCADE ;

CREATE TABLE projet.zone_geo (
    id_zone serial PRIMARY KEY,
    nom text,
    niveau text,
    code_insee text,
    niveau_superieur text
);


--------------------------------------------------------------
-- Composante connexe
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.comp_connexe CASCADE;

CREATE TABLE projet.comp_connexe (
    id_comp_connexe serial PRIMARY KEY
);


--------------------------------------------------------------
-- Polygone
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.polygone CASCADE ;

CREATE TABLE projet.polygone (
    id_polygone serial PRIMARY KEY
);


--------------------------------------------------------------
-- Point
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.point CASCADE ;

CREATE TABLE projet.point (
    id_point serial PRIMARY KEY,
    x float,
    y float,
    unique(x, y)
);


--------------------------------------------------------------
-- Association Zone et Composante connexe
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.asso_zone_comp_co CASCADE ;

CREATE TABLE projet.asso_zone_comp_co (
    id_zone serial references projet.zone_geo,
    id_comp_connexe serial references projet.comp_connexe
);


--------------------------------------------------------------
-- Association Composante connexe et Polygone
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.association_connexe_polygone CASCADE;

CREATE TABLE projet.association_connexe_polygone (
	id_polygone serial references projet.polygone,
    id_comp_connexe serial references projet.comp_connexe,
    ordre serial,
    creux boolean
);


--------------------------------------------------------------
-- Association Polygone et Point
--------------------------------------------------------------

DROP TABLE IF EXISTS projet.association_polygone_point;

CREATE table projet.association_polygone_point (
    id_point serial references projet.point,
    id_polygone serial references projet.polygone,
    ordre serial
);

