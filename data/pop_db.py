import fiona

from src.dao.region_dao import RegionDao
from src.dao.departement_dao import DepartementDao
from src.dao.commune_dao import CommuneDao

from src.dao.point_dao import PointDao
from src.dao.polygone_dao import PolygoneDao

from src.dao.db_connection import DBConnection


with DBConnection().connection as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            "drop sequence if exists seq_id_zone_geo;   "

            "drop sequence if exists seq_id_polygone;   "

            "drop sequence if exists seq_id_point;      "
        )

# Ajout des Régions

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
    "ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00117/"
    "ADE_3-2_SHP_WGS84G_FRA-ED2024-09-18/REGION.shp",
    'r'
) as shapefile:

    schema = shapefile.schema
    print(schema)

    for region in shapefile:
        properties = region["properties"]
        print(properties)
        RegionDao.add_region(properties)

        for polygon in region["geometry"]["coordinates"]:

            PolygoneDao.add_polygone()
            with connection.cursor() as cursor:
                cursor.execute(
                    "drop sequence if exists ordre_point;"

                    "create sequence ordre_point;        "
                )

            for point in polygon:

                PointDao.add_point(point)

                if PointDao.est_dans(point):

                    with connection.cursor() as cursor:
                        cursor.execute(
                            "insert into projet.association_polygone_point  "
                            " (id_point, id_polygone, ordre) values         "
                            " (%(id_point)s),                     "
                            "currval('seq_id_polygone'),                    "
                            "nextval('ordre_point'))                        ",
                            {
                                "id_point": PointDao.get_id_point(point)
                            }
                        )

                else:

                    with connection.cursor() as cursor:
                        cursor.execute(
                            "insert into projet.association_polygone_point  "
                            " (id_point, id_polygone, ordre) values         "
                            " (currval('seq_id_point'),                     "
                            "currval('seq_id_polygone'),                    "
                            "nextval('ordre_point'))                        "
                        )

# Ajout des Départements

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
    "ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00117/"
    "ADE_3-2_SHP_WGS84G_FRA-ED2024-09-18/DEPARTEMENT.shp",
    'r'
) as shapefile:

    schema = shapefile.schema
    print(schema)
    for element in shapefile:
        properties = element["properties"]
        print(properties)
        DepartementDao.add_departement(properties)

# Ajout des Communes

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
    "ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00117/"
    "ADE_3-2_SHP_WGS84G_FRA-ED2024-09-18/COMMUNE.shp",
    'r'
) as shapefile:

    schema = shapefile.schema
    print(schema)
    for element in shapefile:
        properties = element["properties"]
        print(properties)
        CommuneDao.add_commune(properties)
