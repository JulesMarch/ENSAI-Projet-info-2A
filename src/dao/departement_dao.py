from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.business_object.departement import Departement

from src.dao.region_dao import RegionDao
from src.dao.zonage_dao import ZonageDao


class DepartementDao(metaclass=Singleton):
    def add_departement(zone: dict):
        """
        Add a geographical zone to the database
            (works only if the zone is not already in the database)
        """

        # if not ZonageDao.est_dans(zone):

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into projet.zone_geo (nom, niveau,          "
                    " code_insee, niveau_superieur) VALUES              "
                    " (%(nom)s, %(niveau)s, %(code_insee)s,             "
                    " %(niveau_superieur)s)                             ",
                    {
                        "nom": zone["NOM"],
                        "niveau": "Département",
                        "code_insee": zone["INSEE_DEP"],
                        "niveau_superieur": zone["INSEE_REG"]
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

        if res:

            resultat_final = {
                "nom": res["nom"],
                "niveau": res["niveau"],
                "code_insee": res["code_insee"],
                "Région": RegionDao.find_by_code_insee(res["niveau_superieur"])["nom"]
            }

            return resultat_final

        raise ValueError(
                "Le code donné n'est associé à aucun Département."
            )

    def find_by_nom(nom: str):

        resultat_final = None

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                  "
                    " where nom=%(nom)s                             ",
                    {
                        "nom": nom
                    },
                )
                res = cursor.fetchone()

        resultat_final = None

        if res:

            resultat_final = {
                "nom": res["nom"],
                "niveau": res["niveau"],
                "code_insee": res["code_insee"],
                "Région": RegionDao.find_by_code_insee(res["niveau_superieur"])["nom"]
            }

            return resultat_final

    def construction_departement(dep):
        zone = ZonageDao.construction_zonage(dep)
        curr_dep = Departement(
            nom=zone.nom,
            num_dep=dep["code_insee"],
            perimetre=zone.perimetre,
            creux=zone.creux,
            edition_carte=zone.edition_carte
        )
        return curr_dep

    def get_all_dep_in(id_reg):
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "select * from projet.zone_geo                      "
                        " where niveau= 'Département' AND niveau_superieur = %(id)s",
                        {
                            "id": id_reg
                        }
                    )
                    res = cursor.fetchall()
                    return res
