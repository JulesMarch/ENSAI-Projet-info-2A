from utils.singleton import Singleton
from src.dao.db_connection import DBConnection
# from src.business_object.region import Region


class RegionDao(metaclass=Singleton):
    def add_region(zone: dict):
        """
        Add a Region to the database
            (works only if the region is not already in the database)
        """

        # if not ZonageDao.est_dans(zone):

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DO $$                                              "
                    "BEGIN                                              "
                    "   IF NOT EXISTS (SELECT 1 FROM pg_class           "
                    "WHERE relname = 'seq_id_zone_geo') THEN"
                    "   EXECUTE 'CREATE SEQUENCE seq_id_zone_geo';      "
                    "   END IF;                                         "
                    "END $$;                                            "

                    "INSERT INTO projet.zone_geo (nom, niveau,          "
                    " code_insee, niveau_superieur) VALUES              "
                    " (%(nom)s, %(niveau)s,                             "
                    " %(code_insee)s, %(niveau_superieur)s)             ",
                    {
                        "nom": zone["NOM"],
                        "niveau": "Région",
                        "code_insee": zone["INSEE_REG"],
                        "niveau_superieur": "Null"
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
            }

            return resultat_final

        raise ValueError(
                "Le code donné n'est associé à aucune Région."
            )
