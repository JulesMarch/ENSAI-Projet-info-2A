from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.dao.zonage_dao import ZonageDao
from src.dao.commune_dao import CommuneDao
from src.business_object.arrondissement import Arrondissement

import unicodedata


class ArrondissementDao(metaclass=Singleton):
    def add_arrondissement(zone: dict, annee: int):
        """
        Ajoute un Arrondissement Municipal à la base de données.

        Args:
            zone (dict): Dictionnaire contenant les informations de
             l'arrondissement avec les clés "NOM" (nom de l'arrondisement),
              "NOM_M" (nom  en majuscule de l'arrondisement) "INSEE_ARM"
               (code INSEE l'Arrondissement Municipal) et "INSEE_COM" (code
                INSEE de la Commune dans laquelle se troube l'Arrondissement)
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
                        "niveau": "Arrondissement",
                        "code_insee": zone["INSEE_ARM"],
                        "niveau_superieur": zone["INSEE_COM"],
                        "annee": annee
                    },
                )

    def find_by_code_insee(code_insee: str, annee: int) -> dict:
        """
        Récupère les informations d'un Arrondissement à partir de son code

        Args:
            code_insee (str): Code INSEE de l'Arrondissement
            annee: Année de considération

        Returns:
            dict: dictionnaire contenant les informations recherchées
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo where                    "
                    "code_insee=%(code_insee)s and niveau='Arrondissement'  "
                    " and annee=%(annee)s                                   ",
                    {
                        "code_insee": code_insee,
                        "annee": annee
                    },
                )
                res = cursor.fetchone()

        if res is None:
            raise ValueError(
                "Le code donné n'est associé à aucun Iris."
            )

        commune = CommuneDao.find_by_code_insee(
            res["niveau_superieur"], annee
        )

        resultat_final = {
            "nom": res["nom"],
            "niveau": res["niveau"],
            "code_insee": res["code_insee"],
            "Commune": commune["nom"],
            "Département": commune["Département"],
            "Région": commune["Région"],
            "annee": annee
        }

        return resultat_final

    def find_by_nom(nom: str, annee: int) -> dict:
        """
        Récupère les informations d'un Arrondissement à partir de son nom.

        Args:
            nom (str): Nom de l'Arrondissement
            annee: Année de considération

        Returns:
            dict: dictionnaire contenant les informations recherchées
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
                    "select * from projet.zone_geo where                    "
                    "nom_majuscule=%(nom_majuscule)s and                    "
                    "niveau='Arrondissement' and annee=%(annee)s            ",
                    {
                        "nom_majuscule": nom_majuscule,
                        "annee": annee
                    },
                )
                res = cursor.fetchone()

        if res is None:
            raise ValueError(
                "Le code donné n'est associé à aucun Iris."
            )

        commune = CommuneDao.find_by_code_insee(
            res["niveau_superieur"], annee
        )

        resultat_final = {
            "nom": res["nom"],
            "niveau": res["niveau"],
            "code_insee": res["code_insee"],
            "Commune": commune["nom"],
            "Département": commune["Département"],
            "Région": commune["Région"],
            "annee": annee
        }

        return resultat_final

    def construction_arrondissement(arr):
        """
        Construit une instance de la classe Arrondissement à partir
        d'un dictionnaire de données géographiques

        Args:
            arr (dict): Un dictionnaire contenant les informations de
        l'arrondissement et incluant le code INSEE

        Returns:
            Arrondissement: Une instance de la classe Arrondissement
            initialisée avec les données fournies

        """
        zone = ZonageDao.construction_zonage(arr)
        curr_arr = Arrondissement(
            nom=zone.nom,
            num_arr=arr["code_insee"],
            perimetre=zone.perimetre,
            creux=zone.creux,
            edition_carte=zone.edition_carte
        )
        return curr_arr

    def get_all_arr_in(id_com):
        """
        Récupère tous les arrondissements d'une commune spécifique

        Arguments:
            id_com (int): L'identifiant de la commune

        Retour:
        list: Une liste de tous les arrondissements de la commune,
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where niveau= 'Arrondissement' AND    "
                    "niveau_superieur = %(id)s",
                    {
                        "id": id_com
                    }
                )
                res = cursor.fetchall()
                return res
