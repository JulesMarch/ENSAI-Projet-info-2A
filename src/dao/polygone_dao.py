from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection

from src.dao.point_dao import PointDao


class PolygoneDao(metaclass=Singleton):
    def add_polygone(L: list):
        """
        Add a polygone to the database
            (works only if the point is not already in the database)
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into projet.polygone                    "
                    " (region_geo) values (%(region_geo)s);         ",
                    {
                        "region_geo": "Région"
                    }
                )

        for i in range(len(L)):
            PointDao.add_point(L[i])
            id_point = PointDao.get_id_point(L[i])

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "insert into projet.association_polygone_point      "
                        " (id_point, id_polygone, ordre) values             "
                        " (%(id_point)s,                                    "
                        " (select max(id_polygone) from projet.polygone),   "
                        " %(ordre)s)                                        ",
                        {
                            'id_point': id_point,
                            'ordre': i
                        }
                    )
