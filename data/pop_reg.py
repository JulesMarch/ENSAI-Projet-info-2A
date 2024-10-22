import fiona
from src.dao.point_dao import PointDao

L = ["REGION", "DEPARTEMENT", "COMMUNE", "ARRONDISSEMENT"]

for zone in L:

    with fiona.open(
        "//filer-eleves2/id2505/Cours2A/"
        "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
        "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
        "ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00117/"
        "ADE_3-2_SHP_WGS84G_FRA-ED2024-09-18/" + zone + ".shp",
        'r'
    ) as shapefile:

        schema = shapefile.schema
        print(schema)
