from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
# from src.business_object.point import Point


niveaux = ["region", "departement", "commune", "arrondissement", "IRIS"]


class ZonageDao(metaclass=Singleton):
    def add_zone_geo():
        pass

    def find_by_nom(nom: str, niveau: str):
        """
        Find a zonage in the database using the name and the geographic level
        """

        if niveau not in niveaux:
            raise ValueError('le niveau doit être un des suivants: "region",' +
                             '"departement", "commune", "arrondissement",' +
                             '"IRIS"')

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

        resultat_final = []
        for row in res:
            infos = {
                "nom": row["nom"],
                "niveau": row["niveau"],
                "code_insee": row["code_insee"],
                "niveau_superieur": row["niveau_superieur"]
            }
            resultat_final.append(infos)

        return resultat_final

    def find_by_code_insee(code_insee: str, niveau: str):
        """
        Find a zonage in the database using the name and the geographic level
        """
        if niveau not in niveaux:
            raise ValueError('le niveau doit être un des suivants: "region",' +
                             '"departement", "commune", "arrondissement",' +
                             '"IRIS"')

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where code_insee=%(code_insee)s and niveau=%(niveau)s",
                    {
                        "code_insee": code_insee
                    },
                )
                res = cursor.fetchall()

        resultat_final = []
        for row in res:
            infos = {
                "nom": row["nom"],
                "niveau": row["niveau"],
                "code_insee": row["code_insee"],
                "niveau_superieur": row["niveau_superieur"]
            }
            resultat_final.append(infos)

        return resultat_final
