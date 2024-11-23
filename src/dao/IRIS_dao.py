import unicodedata

from src.dao.db_connection import DBConnection
from src.dao.zonage_dao import ZonageDao
from src.business_object.IRIS import Iris
from src.dao.commune_dao import CommuneDao
from src.utils.conversion import Conversion


class IrisDao(ZonageDao):
    def add_iris(zone: dict, annee: int):
        """
        Add a geographical zone to the database
            (works only if the zone is not already in the database)
        """

        # On convertit le nom en majuscule
        nom_maj = zone["NOM_IRIS"].upper()

        # On retire les accents
        nom__maj_sans_accents = ''.join(
            c for c in unicodedata.normalize('NFD', nom_maj)
            if unicodedata.category(c) != 'Mn'
        )

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into projet.zone_geo (nom, nom_majuscule,   "
                    "niveau, code_insee, niveau_superieur, annee) VALUES"
                    " (%(nom)s, %(nom__maj_sans_accents)s, %(niveau)s,  "
                    " %(code_insee)s, %(niveau_superieur)s, %(annee)s)  ",
                    {
                        "nom": zone["NOM_IRIS"],
                        "nom__maj_sans_accents": nom__maj_sans_accents,
                        "niveau": "Iris",
                        "code_insee": zone["CODE_IRIS"],
                        "niveau_superieur": zone["INSEE_COM"],
                        "annee": annee
                    },
                )

    def find_by_code_insee(code_insee: str, annee: int):
        """
        Récupère les informations d'une zone IRIS à partir de son code

        Args:
            niveau (str): Niveau géographique de la zone
            code (int): Code INSEE de la zone IRIS

        Returns:
            str: Description de la zone IRIS avec son nom et sa localisation
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                          "
                    " where code_insee=%(code_insee)s and niveau='Iris'     "
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

    def find_by_nom(nom: str, annee: int):
        """
        Récupère les informations d'une zone IRIS à partir de son code

        Args:
            niveau (str): Niveau géographique de la zone
            code (int): Code INSEE de la zone IRIS

        Returns:
            str: Description de la zone IRIS avec son nom et sa localisation
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
                    " where nom_majuscule=%(nom_majuscule)s and niveau='Iris'"
                    " and annee=%(annee)s                                   ",
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

    def construction_IRIS(iris):
        """
        Construit une instance de la classe Iris à partir
        d'un dictionnaire de données géographiques

        Args:
            arr (dict): Un dictionnaire contenant les informations de
        l'arrondissement et incluant le code INSEE

        Returns:
            Iris: Une instance de la classe Iris
            initialisée avec les données fournies

        """
        zone = ZonageDao.construction_zonage(iris)
        curr_iris = Iris(
            nom=zone.nom,
            num_iris=iris["code_insee"],
            perimetre=zone.perimetre,
            creux=zone.creux,
            edition_carte=zone.edition_carte
        )
        return curr_iris

    def get_all_iris_in(id_com):
        """
        Récupère tous les iris d'une commune spécifique

        Arguments:
            id_com (int): L'identifiant de la commune

        Retour:
        list: Une liste de tous les iris de la commune,
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where niveau= 'Iris' AND    "
                    "niveau_superieur = %(id)s",
                    {
                        "id": id_com
                    }
                )
                res = cursor.fetchall()
                return res


# test = IrisDao.find_by_code("352380510", 2023)
# print(test)
