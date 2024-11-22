from src.dao.db_connection import DBConnection
from src.dao.zonage_dao import ZonageDao
from src.business_object.IRIS import Iris


class IrisDao(ZonageDao):
    def add_iris(zone: dict, annee: int):
        """
        Add a geographical zone to the database
            (works only if the zone is not already in the database)
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into projet.zone_geo (nom, nom_majuscule,   "
                    "niveau, code_insee, niveau_superieur, annee) VALUES"
                    " (%(nom)s, upper(%(nom)s), %(niveau)s,          "
                    " %(code_insee)s, %(niveau_superieur)s, %(annee)s)  ",
                    {
                        "nom": zone["NOM_IRIS"],
                        "niveau": "Iris",
                        "code_insee": zone["CODE_IRIS"],
                        "niveau_superieur": zone["INSEE_COM"],
                        "annee": annee
                    },
                )

    def find_by_code(self, niveau: str, code: int):
        """
        Récupère les informations d'une zone IRIS à partir de son code

        Args:
            niveau (str): Niveau géographique de la zone
            code (int): Code INSEE de la zone IRIS

        Returns:
            str: Description de la zone IRIS avec son nom et sa localisation
        """
        request = (
            f"SELECT code_insee, nom, zone_superieur"
            f"FROM projet.zone_geo"
            f"WHERE code_insee = {code}"
        )

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(request)
                res = cursor.fetchone()

        informations = (
            f"Le code {res['code_insee']} correspond à la zone "
            f"IRIS {res['nom']} situé en"
            f"{res['niveau_superieur']}")
        return informations

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
