from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.business_object.departement import Departement

from src.dao.region_dao import RegionDao
from src.dao.zonage_dao import ZonageDao


class DepartementDao(metaclass=Singleton):
    def add_departement(zone: dict):
        """
        Ajoute une zone géographique à la base de donnée
        
        Args:
            zone (dict): Dictionnaire contenant les informations sur 
            la zone avec les clés "NOM", "INSEE_DEP", et "INSEE_REG"
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
        Trouve un zonage dans la base de données en utilisant un nom et un niveau géographique

       Args:
        code_insee (str): Code INSEE de la zone à rechercher.

        Returns:
            dict: Dictionnaire contenant les informations de la zone,
              incluant le nom, le niveau, le code INSEE, et la région. 
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
                "Région": RegionDao.find_by_code_insee(
                    res["niveau_superieur"])["nom"]
            }

            return resultat_final

        raise ValueError(
                "Le code donné n'est associé à aucun Département."
            )

    def find_by_nom(nom: str):
       """
        Recherche une zone géographique dans la base de données par son nom

        Args:
            nom (str): Nom de la zone à rechercher

        Returns:
         dict: Dictionnaire contenant les informations de la zone,
              incluant le nom, le niveau, le code INSEE, et la région
        """
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
                "Région": RegionDao.find_by_code_insee(
                    res["niveau_superieur"])["nom"]
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
