from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection


class DepartementDao(metaclass=Singleton):
    def add_zone_geo(zone: dict):
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
                    "code_insee, niveau_superieur)"
                    "SELECT"
                    " (nextval('seq_id_zone_geo'), %(nom)s, %(niveau)s, "
                    " %(code_insee)s,"
                    "(SELECT nom FROM projet.zone_geo WHERE code_insee = %(niveau_superieur)s)",
                    {
                        "nom": zone["NOM"],
                        "niveau": "Département",
                        "code_insee": zone["INSEE_DEP"],
                        "niveau_superieur": zone["INSEE_REG"]
                    },
                )
