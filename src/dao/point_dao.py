from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection

from src.business_object.point import Point


class PointDao(metaclass=Singleton):
    def add_point(point: tuple):
        """
        Add a point to the database
            (works only if the point is not already in the database)
        """

        if not PointDao.est_dans(point):

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DO $$                                              "
                        "BEGIN                                              "
                        "   IF NOT EXISTS (SELECT 1 FROM pg_class           "
                        "WHERE relname = 'seq_id_point') THEN"
                        "   EXECUTE 'CREATE SEQUENCE seq_id_point';         "
                        "   END IF;                                         "
                        "END $$;                                            "

                        "INSERT INTO projet.point (id_point, x, y) VALUES   "
                        " (nextval('seq_id_point'), %(x)s, %(y)s);          ",
                        {
                            "x": point[0],
                            "y": point[1]
                        },
                    )

    def est_dans(point: tuple) -> bool:
        """
        Tell if a point is in the database
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select x, y from projet.point                          "
                    "   where x=%(x)s and y=%(y)s                           ",
                    {
                        "x": round(point[0], 4),
                        "y": round(point[1], 4)
                    },
                )
                res = cursor.fetchone()

        if res is not None:

            return True

        return False

    def get_point(self, id: int) -> Point:

        point = None

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select x, y from projet.point                          "
                    "   where id_point=%(id)s                               ",
                    {
                        "id_point": id
                    },
                )
                res = cursor.fetchone()

        if res:
            point = Point(
                x=res["x"],
                y=res["y"]
            )

        return point

    def get_id_point(point: tuple) -> int:

        id = None

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select id from projet.point                          "
                    "   where x=%(x)s, y=%(y)s                            ",
                    {
                        "x": point[0],
                        "y": point[1]
                    },
                )
                res = cursor.fetchone()

        if res:

            id = res["id"]

        return id
