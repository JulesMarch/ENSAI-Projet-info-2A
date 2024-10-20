import fiona
from src.dao.db_connection import DBConnection

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/" +
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/" +
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/" +
    "ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00117/" +
    "ADE_3-2_SHP_WGS84G_FRA-ED2024-09-18/REGION.shp",
    'r'
) as shapefile:
    i = 0
    for element in shapefile:
        i += 1
        properties = element["properties"]
        geometry = element["geometry"]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO projet.zone_geo (id_zone, nom, niveau,     "
                    " code_insee, niveau_supperieur) VALUES                 "
                    "(%(id_zone)s, %(nom)s, 'Région',                       "
                    " %(code_insee)s, 'blabla')                             ",
                    {
                        "id_zone": i,
                        "nom": properties["NOM"],
                        "code_insee": properties["INSEE_REG"],
                    },
                )
