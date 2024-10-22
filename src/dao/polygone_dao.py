from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection


class PolygoneDao(metaclass=Singleton):
    def add_polygone():
        """
        Add a polygone to the database
            (works only if the point is not already in the database)
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DO $$                                              "
                    "BEGIN                                              "
                    "   IF NOT EXISTS (SELECT 1 FROM pg_class           "
                    "WHERE relname = 'seq_id_polygone') THEN"
                    "   EXECUTE 'CREATE SEQUENCE seq_id_polygone';      "
                    "   END IF;                                         "
                    "END $$;                                            "

                    "INSERT INTO projet.polygone (id_polygone) VALUES   "
                    " (nextval('seq_id_polygone'))                      ",
                )
