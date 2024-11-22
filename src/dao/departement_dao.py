import unicodedata

from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.business_object.departement import Departement

from src.dao.region_dao import RegionDao
from src.dao.zonage_dao import ZonageDao


class DepartementDao(metaclass=Singleton):
    def add_departement(zone: dict, annee: int):
        """
        Ajoute une zone géographique à la base de donnée

        Args:
            zone (dict): Dictionnaire contenant les informations sur
            la zone avec les clés "NOM", "INSEE_DEP", et "INSEE_REG"
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
                        "niveau": "Département",
                        "code_insee": zone["INSEE_DEP"],
                        "niveau_superieur": zone["INSEE_REG"],
                        "annee": annee
                    },
                )

    def find_by_code_insee(code_insee: str, annee: int):
        """
        Trouve un zonage dans la base de données en utilisant un nom
         et un niveau géographique

       Args:
        code_insee (str): Code INSEE de la zone à rechercher.

        Returns:
            dict: Dictionnaire contenant les informations de la zone,
              incluant le nom, le niveau, le code INSEE, et la région.
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                           "
                    "where code_insee=%(code_insee)s and niveau='Département'"
                    " and annee=%(annee)s                                    ",
                    {
                        "code_insee": code_insee,
                        "annee": annee
                    },
                )
                res = cursor.fetchone()

        if res is None:
            raise ValueError(
                "Le code donné n'est associé à aucun Département."
            )

        region = RegionDao.find_by_code_insee(
            res["niveau_superieur"], annee
        )["nom"]

        resultat_final = {
            "nom": res["nom"],
            "niveau": res["niveau"],
            "code_insee": res["code_insee"],
            "Région": region,
            "annee": annee
        }

        return resultat_final

    def find_by_nom(nom: str, annee: int):
        """
        Recherche une zone géographique dans la base de données par son nom

        Args:
            nom (str): Nom de la zone à rechercher

        Returns:
         dict: Dictionnaire contenant les informations de la zone,
              incluant le nom, le niveau, le code INSEE, et la région
        """

        # On convertit le nom en majuscule
        nom = nom.upper()

        # On retire les accents
        nom_majuscule = ''.join(
            c for c in unicodedata.normalize('NFD', nom)
            if unicodedata.category(c) != 'Mn'
        )

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                          "
                    " where nom_majuscule=%(nom_majuscule)s                 "
                    " and niveau='Département' and annee=%(annee)s          ",
                    {
                        "nom_majuscule": nom_majuscule,
                        "annee": annee
                    },
                )
                res = cursor.fetchone()

        if res is None:
            raise ValueError(
                "Le nom donné n'est associé à aucun Département."
            )

        region = RegionDao.find_by_code_insee(
            res["niveau_superieur"], annee
        )["nom"]

        resultat_final = {
            "nom": res["nom"],
            "niveau": res["niveau"],
            "code_insee": res["code_insee"],
            "Région": region
        }

        return resultat_final

    def construction_departement(dep):
        """
        Construit un objet département à partir des données fournies

        Args:
            dep (dict): Dictionnaire contenant les informations
            du département

        Returns:
            Departement: Objet représentant le département avec ses
            attributs (nom, numéro, périmètre, creux, édition de carte)
        """
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
        """
        Récupère tous les départements appartenant à une région donnée

        Args:
            id_reg (int): Identifiant de la région (code INSEE)

        Returns:
            list[dict]: Liste des départements sous forme de
            dictionnaires contenant leurs attributs
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where niveau= 'Département' AND niveau_superieur"
                    " = %(id)s",
                    {
                        "id": id_reg
                    }
                )
                res = cursor.fetchall()
                return res


# test = DepartementDao.find_by_code_insee("01", 2023)
# print(test)
