from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.dao.departement_dao import DepartementDao
from src.dao.zonage_dao import ZonageDao
from src.business_object.commune import Commune


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
                    " where code_insee=%(code_insee)s                       ",
                    {
                        "code_insee": code_insee
                    },
                )
                res = cursor.fetchone()

        resultat_final = None

        if res is None:
            raise ValueError(
                "Le code donné n'est associé à aucune Commune."
            )

        departement = DepartementDao.find_by_code_insee(
            res["niveau_superieur"])

        if res:

            resultat_final = {
                "nom": res["nom"],
                "niveau": res["niveau"],
                "code_insee": res["code_insee"],
                "Département": departement["nom"],
                "Région": departement["Région"]
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
        zone = ZonageDao.construction_zonage(com)
        curr_com = Commune(
            nom=zone.nom,
            code_postal=com["code_insee"],
            perimetre=zone.perimetre,
            creux=zone.creux,
            edition_carte=zone.edition_carte
        )
        return curr_com

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

        departement = DepartementDao.find_by_code_insee(
            res["niveau_superieur"])

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
