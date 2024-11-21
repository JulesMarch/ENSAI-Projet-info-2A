import fiona

from src.dao.arrondissement_dao import ArrondissementDao

from src.dao.composante_connexe_dao import ComposanteConnexeDao


# Ajout des Arrondissements Communaux

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG/1_DONNEES_LIVRAISON_2023-05-03/"
    "ADECOG_3-2_SHP_WGS84G_FRA/ARRONDISSEMENT_MUNICIPAL.shp",
    'r'
) as shapefile:

    for iris in shapefile:

        # Dictionnaire contenant les informations de la commune
        properties = iris["properties"]
        print(properties)

        # Dictionnaire contenant les délimitations de la commune
        geometry = iris['geometry']

        # Remplissage des informations liées à la commune
        ArrondissementDao.add_arrondissement(properties)

        # Remplissage des contours geographiques du département
        ComposanteConnexeDao.add_composante_connexe(
            geometry["coordinates"],
            geometry["type"]
        )
