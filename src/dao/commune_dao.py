from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection

from src.dao.region_dao import RegionDao
from src.dao.departement_dao import DepartementDao


class CommuneDao(metaclass=Singleton):
    def add_commune(zone: dict):
        """
        Add a geographical zone to the database
            (works only if the zone is not already in the database)
        """

        # if not ZonageDao.est_dans(zone):

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO projet.zone_geo (nom, niveau, "
                    " code_insee, niveau_superieur) VALUES              "
                    " (%(nom)s, %(niveau)s, %(code_insee)s,             "
                    "%(niveau_superieur)s)                              ",
                    {
                        "nom": zone["NOM"],
                        "niveau": "Commune",
                        "code_insee": zone["INSEE_COM"],
                        "niveau_superieur": zone["INSEE_DEP"]
                    },
                )

    def find_by_code_insee(code_insee: str):
        """
        Find a zonage in the database using the name and the geographic level
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                          "
                    " where code_insee=%(code_insee)s                       ",
                    {
                        "code_insee": code_insee
                    },
                )
                res = cursor.fetchone()

        resultat_final = None

        departement = DepartementDao.find_by_code_insee(res["niveau_superieur"])

        if res:

            resultat_final = {
                "nom": res["nom"],
                "niveau": res["niveau"],
                "code_insee": res["code_insee"],
                "Département": departement["nom"],
                "Région": departement["Région"]
            }

            return resultat_final

        raise ValueError(
                "Le code donné n'est associé à aucune Région."
            )

    def find_by_nom(nom: str):

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo      "
                    " where nom=%(nom)s                 ",
                    {
                        "nom": nom
                    },
                )
                res = cursor.fetchone()

        resultat_final = None

        departement = DepartementDao.find_by_code_insee(res["niveau_superieur"])

        if res:

            resultat_final = {
                "nom": res["nom"],
                "niveau": res["niveau"],
                "code_insee": res["code_insee"],
                "Département": departement["nom"],
                "Région": departement["Région"]
            }

            return resultat_final

        raise ValueError(
                "Le nom donné n'est associé à aucune Région."
            )
