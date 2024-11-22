import fiona

from src.dao.IRIS_dao import IrisDao

from src.dao.composante_connexe_dao import ComposanteConnexeDao


# Ajout des Iris
with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "CONTOURS-IRIS_3-0__SHP__FRA_2023-01-01/"
    "CONTOURS-IRIS_3-0__SHP__FRA_2023-01-01/"
    "CONTOURS-IRIS/1_DONNEES_LIVRAISON_2024-02-00238/"
    "CONTOURS-IRIS_3-0_SHP_LAMB93_FXX-ED2023-01-01/CONTOURS-IRIS.shp",
    'r'
) as shapefile:

    for iris in shapefile:

        # Dictionnaire contenant les informations de l'iris
        properties = iris["properties"]
        print(properties)

        # Dictionnaire contenant les délimitations l'iris
        geometry = iris['geometry']

        # Remplissage des informations liées l'iris
        IrisDao.add_iris(properties, 2023)

        # Remplissage des contours geographiques de l'iris
        ComposanteConnexeDao.add_composante_connexe(
            geometry["coordinates"],
            geometry["type"]
        )
