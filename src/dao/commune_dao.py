import unicodedata

from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.dao.departement_dao import DepartementDao
from src.dao.zonage_dao import ZonageDao
from src.business_object.commune import Commune


class CommuneDao(metaclass=Singleton):
    def add_commune(zone: dict, annee: int):
        """
        Add a geographical zone to the database
            (works only if the zone is not already in the database)
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
                        "niveau": "Commune",
                        "code_insee": zone["INSEE_COM"],
                        "niveau_superieur": zone["INSEE_DEP"],
                        "annee": annee
                    },
                )

    def find_by_code_insee(code_insee: str, annee: int):
        """
        Trouve un zonage dans la base de données en utilisant le code INSEE.

        Args:
            code_insee (str): Code INSEE de la zone recherchée.

        Returns:
            dict: Dictionnaire avec le nom, le niveau, le code INSEE,
                  le département et la région associés. Lève une
                  erreur si aucune zone n'est trouvée.
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                          "
                    " where code_insee=%(code_insee)s and niveau='Commune'  "
                    " and annee=%(annee)s                                   ",
                    {
                        "code_insee": code_insee,
                        "annee": annee
                    },
                )
                res = cursor.fetchone()

        resultat_final = None

        if res is None:
            raise ValueError(
                "Le code donné n'est associé à aucune Commune."
            )

        departement = DepartementDao.find_by_code_insee(
            res["niveau_superieur"], annee
        )

        resultat_final = {
            "nom": res["nom"],
            "niveau": res["niveau"],
            "code_insee": res["code_insee"],
            "Département": departement["nom"],
            "Région": departement["Région"],
            "année": annee
        }

        return resultat_final

    def find_by_nom(nom: str, annee: int):
        """
        Recherche une zone géographique par son nom

        Args:
            nom (str): Nom de la zone recherchée

        Returns:
            dict: Informations sur la zone, y compris le département
             et la région
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
                    " and niveau='Commune' and annee=%(annee)s              ",
                    {
                        "nom_majuscule": nom_majuscule,
                        "annee": annee
                    },
                )
                res = cursor.fetchone()

        resultat_final = None

        if res is None:
            raise ValueError(
                "Le nom donné n'est associé à aucune Commune."
            )

        departement = DepartementDao.find_by_code_insee(
            res["niveau_superieur"], annee
        )

        resultat_final = {
            "nom": res["nom"],
            "niveau": res["niveau"],
            "code_insee": res["code_insee"],
            "Département": departement["nom"],
            "Région": departement["Région"],
            "année": annee
        }

        return resultat_final

    def get_all_com_in(id_dep):
        """
        Récupère toutes les communes d'un département spécifique

        Arguments:
            id_dep (int): L'identifiant du département

        Retour:
        list: Une liste de toutes les communes du département,
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where niveau= 'Commune' AND niveau_superieur = %(id)s",
                    {
                        "id": id_dep
                    }
                )
                res = cursor.fetchall()
                return res

    def construction_commune(com):
        """
        Construit une instance de la classe Commune à partir
        d'un dictionnaire de données géographiques

        Args:
            com (dict): Un dictionnaire contenant les informations de
             la commune et incluant le code INSEE

         Returns:
            Commune: Une instance de la classe Commune initialisée avec les
            données fournies

        """
        zone = ZonageDao.construction_zonage(com)
        curr_com = Commune(
            nom=zone.nom,
            code_postal=com["code_insee"],
            perimetre=zone.perimetre,
            creux=zone.creux,
            edition_carte=zone.edition_carte
        )
        return curr_com


# test = CommuneDao.find_by_nom("Bezac", 2023)
# print(test)
