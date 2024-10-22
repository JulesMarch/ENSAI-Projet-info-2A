# from utils.singleton import Singleton
# from dao.db_connection import DBConnection
from zonage_dao import ZonageDao
# from src.business_object.region import Region


class RegionDao(ZonageDao):
    def add_region_geo(zone: dict):
        """
        Add a geographical zone to the database
            (works only if the zone is not already in the database)
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

                    "INSERT INTO projet.zone_geo (id_zone, nom, niveau, "
                    " code_insee, niveau_superieur) VALUES              "
                    " (nextval('seq_id_zone_geo'), %(nom)s, %(niveau)s, "
                    " %(code_insee)s, %(niveau_superieur)s)             ",
                    {
                        "nom": zone["NOM"],
                        "niveau": "Région",
                        "code_insee": zone["INSEE_REG"],
                        "niveau_superieur": "Null"
                    },
                )
