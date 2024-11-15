import fiona

from src.dao.departement_dao import DepartementDao
from src.dao.composante_connexe_dao import ComposanteConnexeDao


with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG/1_DONNEES_LIVRAISON_2023-05-03/"
    "ADECOG_3-2_SHP_WGS84G_FRA/DEPARTEMENT.shp",
    'r'
) as shapefile:

    schema = shapefile.schema
    print(schema)

    for departement in shapefile:

        # Dictionnaire contenant les informations du département
        properties = departement["properties"]
        print(properties)

        # Dictionnaire contenant les délimitations du département
        geometry = departement['geometry']
        print(geometry)

        # Remplissage des informations liées au département
        DepartementDao.add_departement(properties)

        # Remplissage des contours geographiques du département
        ComposanteConnexeDao.add_composante_connexe(
            geometry["coordinates"],
            geometry["type"]
        )