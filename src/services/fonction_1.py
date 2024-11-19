from src.dao.region_dao import RegionDao
from src.dao.departement_dao import DepartementDao
from src.dao.commune_dao import CommuneDao
from src.dao.db_connection import DBConnection

niveaux_possibles = ["Commune", "Département", "Région"]


def find_by_code_insee(code_insee: str, niveau: str):
    """
    Find a zonage in the database using the code and the geographic level
    """

    if niveau not in niveaux_possibles:
        raise ValueError(f'Le niveau doit être dans {niveaux_possibles}')

    code_insee = str(code_insee)

    if niveau == "Région":
        return RegionDao.find_by_code_insee(code_insee)

    elif niveau == "Département":
        return DepartementDao.find_by_code_insee(code_insee)

    elif niveau == "Commune":
        return CommuneDao.find_by_code_insee(code_insee)


def find_by_nom(nom: str, niveau: str):
    """
    Find a zonage in the database using the name and the geographic level
    """

    if niveau not in niveaux_possibles:
        raise ValueError(f'Le niveau doit être dans {niveaux_possibles}')

    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from projet.zone_geo                      "
                " where nom=%(nom)s and niveau=%(niveau)s           ",
                {
                    "nom": nom,
                    "niveau": niveau
                },
            )
            res = cursor.fetchall()

    if len(res) == 0:
        raise ValueError("Ce nom est introuvable dans la base de données")

    for row in res:
        print(row)
        infos = {
            "nom": row["nom"],
            "niveau": row["niveau"],
            "code_insee": row["code_insee"],
            "niveau_superieur": row["niveau_superieur"]
        }
        return infos
