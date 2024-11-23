import fiona

from src.dao.commune_dao import CommuneDao

from src.dao.composante_connexe_dao import ComposanteConnexeDao


# Ajout des Communes

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG/1_DONNEES_LIVRAISON_2023-05-03/"
    "ADECOG_3-2_SHP_WGS84G_FRA/COMMUNE.shp",
    'r'
) as shapefile:

    for commune in shapefile:

        # Dictionnaire contenant les informations de la commune
        properties = commune["properties"]
        print(properties)

        # Dictionnaire contenant les délimitations de la commune
        geometry = commune['geometry']

        # Remplissage des informations liées à la commune
        CommuneDao.add_commune(properties, 2023)

        # Remplissage des contours geographiques de la commune
        ComposanteConnexeDao.add_composante_connexe(
            geometry["coordinates"],
            geometry["type"]
        )
