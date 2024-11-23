from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection

from src.dao.point_dao import PointDao


class PolygoneDao(metaclass=Singleton):
    def add_polygone(L: list):
        """
        Ajoute un polygone à la base de données en associant ses points

        Args:
            L (list): Liste des points du polygone, chaque point étant un
            tuple (x, y).
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
