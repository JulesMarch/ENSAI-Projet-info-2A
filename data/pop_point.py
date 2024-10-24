import fiona
from src.dao.point_dao import PointDao

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/" +
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/" +
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-09-18/" +
    "ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09-00117/" +
    "ADE_3-2_SHP_WGS84G_FRA-ED2024-09-18/REGION.shp",
    'r'
) as shapefile:

    for element in shapefile:
        for polygon in element["geometry"]["coordinates"]:
            for point in polygon:

                PointDao.add_point(point)
