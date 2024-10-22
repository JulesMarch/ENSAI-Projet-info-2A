from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection


class ComposanteConnexeDao(metaclass=Singleton):
    def add_composante_connexe():
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
                    "WHERE relname = 'seq_id_comp_co') THEN"
                    "   EXECUTE 'CREATE SEQUENCE seq_id_comp_co';      "
                    "   END IF;                                         "
                    "END $$;                                            "

                    "INSERT INTO projet.comp_connexe (id_comp_connexe)  "
                    " VALUES                                            "
                    " (nextval('seq_id_comp_co'))                      ",
                )
