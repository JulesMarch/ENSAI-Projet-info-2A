from src.utils.singleton import Singleton
from src.business_object.region import Region
from src.dao.db_connection import DBConnection
from src.dao.zonage_dao import ZonageDao


class RegionDao(metaclass=Singleton):
    def add_region(zone: dict, annee):
        """
        Ajoute une région à la base de données

        Args:
            zone (dict): Dictionnaire contenant les informations de la région
             avec les clés "NOM" (nom de la région), "INSEE_REG" (code INSEE
              de la région)
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into projet.zone_geo (nom, nom_majuscule,   "
                    "niveau, code_insee, niveau_superieur, annee) VALUES"
                    " (%(nom)s, %(nom_majuscule)s, %(niveau)s,          "
                    " %(code_insee)s, %(niveau_superieur)s, %(annee)s)  ",
                    {
                        "nom": zone["NOM"],
                        "nom_majuscule": zone["NOM_M"],
                        "niveau": "Région",
                        "code_insee": zone["INSEE_REG"],
                        "niveau_superieur": "Null",
                        "annee": annee
                    },
                )

    def find_by_code_insee(code_insee: str):
        """
        Trouve un zonage dans la base de données à partir de son code INSEE

        Args:
            code_insee (str): Code INSEE de la zone géographique

        Returns:
            dict: Informations sur le zonage, incluant son nom, niveau et
             code INSEE
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                          "
                    " where code_insee=%(code_insee)s and niveau='Région'   ",
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
            }

            return resultat_final

        raise ValueError(
                "Le code donné n'est associé à aucune Région."
            )

    def get_all_regions():
        """
        Récupère toutes les régions de la base de données

        Returns:
            list: Liste des régions, chaque élément contenant
             les informations de la région
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where niveau= 'Région'                            ",
                )
                res = cursor.fetchall()
                return res

    def construction_region(reg):
        """
        Construit un objet Région à partir des données fournies

        Args:
            reg (dict): Dictionnaire contenant les informations de la région,

        Returns:
            Region: Objet représentant la région avec ses attributs
             (nom, numéro, périmètre, etc.)
        """
        zone = ZonageDao.construction_zonage(reg)
        curr_reg = Region(
            nom=zone.nom,
            num_rgn=reg["code_insee"],
            perimetre=zone.perimetre,
            creux=zone.creux,
            edition_carte=zone.edition_carte
        )
        return curr_reg
