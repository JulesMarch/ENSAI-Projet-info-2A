from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection

from src.dao.polygone_dao import PolygoneDao


class ComposanteConnexeDao(metaclass=Singleton):
    def add_composante_connexe(L: list, type_composante: str):
        """
        Add a polygone to the database
            (works only if the point is not already in the database)
        """

        if type_composante == 'Polygon':

            for k in range(len(L)):

                polygon = L[k]
                PolygoneDao.add_polygone(polygon)

                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "insert into projet.comp_connexe                "
                            "(type_composante) values (%(type_composante)s);"

                            "insert into projet.association_connexe_polygone"
                            " (id_polygone, id_comp_connexe, ordre, creux)  "
                            "values                                         "
                            "((select max(id_polygone) from projet.polygone),"
                            "(select max(id_comp_connexe) from              "
                            "projet.comp_connexe), %(ordre)s, %(creux)s)    ",
                            {
                                'type_composante': type_composante,
                                'ordre': k,
                                'creux': False
                            }
                        )
