import fiona
from src.dao.departement_dao import DepartementDao
from src.dao.commune_dao import CommuneDao

# with fiona.open(
#     "//filer-eleves2/id2505/Cours2A/"
#     "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
#     "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
#     "ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00117/"
#     "ADE_3-2_SHP_WGS84G_FRA-ED2024-09-18/REGION.shp",
#     'r'
# ) as shapefile:

#     schema = shapefile.schema
#     print(schema)
#     for element in shapefile: 
#         properties = element["properties"]
#         print(properties)
#         ZonageDao.add_zone_geo(properties)


# with fiona.open(
#     "//filer-eleves2/id2505/Cours2A/"
#     "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
#     "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/"
#     "ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00117/"
#     "ADE_3-2_SHP_WGS84G_FRA-ED2024-09-18/DEPARTEMENT.shp",
#     'r'
# ) as shapefile:

#     schema = shapefile.schema
#     print(schema)
#     for element in shapefile: 
#         properties = element["properties"]
#         print(properties)
#         DepartementDao.add_zone_geo(properties)

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
        CommuneDao.add_zone_geo(properties)