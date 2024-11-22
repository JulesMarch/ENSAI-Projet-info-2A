from src.dao.region_dao import RegionDao
from src.dao.departement_dao import DepartementDao
from src.dao.commune_dao import CommuneDao
from src.dao.db_connection import DBConnection

niveaux_possibles = ["Commune", "Département", "Région", "Arrondissement",
                     "IRIS"]


def find_by_code_insee(code_insee: str, niveau: str, annee: int):
    """
    Recherche un zonage dans la base de données à partir du code INSEE
    et du niveau géographique.

    Args :
        code_insee (str) : Le code INSEE (pour la commune, le département
         ou la région)
        niveau (str) : Le niveau géographique ("Région", "Département",
         ou "Commune")

    Returns :
        Objet : Un objet correspondant à la région, au département
        ou à la commune trouvée dans la base de données

    Raise :
        ValueError : Si le niveau n'est pas valide
    """

    if niveau not in niveaux_possibles:
        raise ValueError(f'Le niveau doit être dans {niveaux_possibles}')

    if annee != 2023:
        raise ValueError(
            "Pour des raisons de volumétrie de données, "
            "seule l'année 2023 est acceptée pour le moment."
        )

    code_insee = str(code_insee)

    if niveau == "Région":
        return RegionDao.find_by_code_insee(code_insee, annee)

    elif niveau == "Département":
        return DepartementDao.find_by_code_insee(code_insee, annee)

    elif niveau == "Commune":
        return CommuneDao.find_by_code_insee(code_insee, annee)


def find_by_nom(nom: str, niveau: str, annee: int):
    """
    Recherche un zonage par nom et niveau dans la base de données

    Args:
        nom (str): Le nom de la zone géographique à rechercher
        niveau (str): Le niveau géographique de la zone

    Returns:
        dict: Un dictionnaire contenant les informations de la zone,
        avec les clés "nom", "niveau", "code_insee", et "niveau_superieur"

    Raise:
        ValueError: Si le niveau fourni n'est pas valide ou si aucun
         zonage n'est trouvé pour le nom et le niveau spécifiés
    """

    if niveau not in niveaux_possibles:
        raise ValueError(f'Le niveau doit être dans {niveaux_possibles}')

    if annee != 2023:
        raise ValueError(
            "Pour des raisons de volumétrie de données, "
            "seule l'année 2023 est acceptée pour le moment."
        )

    if niveau == "Région":
        return RegionDao.find_by_nom(nom, annee)

    elif niveau == "Département":
        return DepartementDao.find_by_nom(nom, annee)

    elif niveau == "Commune":
        return CommuneDao.find_by_nom(nom, annee)


test = find_by_code_insee("07", "Département", 2023)
print(test)