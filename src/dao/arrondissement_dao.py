from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.dao.zonage_dao import ZonageDao
from src.business_object.arrondissement import Arrondissement


class ArrondissementDao(metaclass=Singleton):
    def add_arrondissement(zone: dict, annee: int):
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
                        "niveau": "Arrondissement",
                        "code_insee": zone["INSEE_ARM"],
                        "niveau_superieur": zone["INSEE_COM"],
                        "annee": annee
                    },
                )

    def find_by_code_insee(code: str, annee: int):
        """
        Recherche des informations sur un arrondissement à partir de son code
        INSEE

        Args:
            niveau (str): Niveau géographique (ex : "commune")
            code (int): Code INSEE de la zone à rechercher

        Returns:
            str: Informations sur l'arrondissement, incluant le code INSEE,
                 le nom de la commune et la zone supérieure.
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
            f"Le code {res['code_insee']} correspond à l'arrondissement"
            f"commune {res['nom']} situé en {res['niveau_superieur']}")
        return informations

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
