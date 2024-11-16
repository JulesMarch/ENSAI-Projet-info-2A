import fiona

from src.dao.region_dao import RegionDao

from src.dao.composante_connexe_dao import ComposanteConnexeDao


# Ajout des Régions

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG/1_DONNEES_LIVRAISON_2023-05-03/"
    "ADECOG_3-2_SHP_WGS84G_FRA/REGION.shp",
    'r'
) as shapefile:

    for region in shapefile:

        # Dictionnaire contenant les informations de la région
        properties = region["properties"]
        print(properties)

        # Dictionnaire contenant les délimitations de la région
        geometry = region['geometry']

        if geometry["type"] == "MultiPolygon":
            # Remplissage des informations liées à la région
            RegionDao.add_region(properties)

            # Remplissage des contours geographiques de la région
            ComposanteConnexeDao.add_composante_connexe(
                geometry["coordinates"],
                geometry["type"]
            )
