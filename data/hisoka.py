import fiona
from src.dao.zonage_dao import ZonageDao


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

    properties = shapefile["properties"]
