from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection

from src.business_object.point import Point


class PointDao(metaclass=Singleton):
    def add_point(point: tuple):
        """
        Ajoute un point à la base de données si celui-ci n'y est pas déjà

        Args:
            point (tuple): Coordonnées du point sous la forme (x, y)
        """
        print("Ajout point :)")
        if not PointDao.est_dans(point):

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO projet.point (x, y) VALUES   "
                        " (%(x)s, %(y)s);          ",
                        {
                            "x": point[0],
                            "y": point[1]
                        },
                    )
                connection.commit()
        print("Réussite")

    def est_dans(point: tuple) -> bool:
        """
        Vérifie si un point existe déjà dans la base de données

        Args:
            point (tuple): Coordonnées du point sous la forme (x, y)

        Returns:
            bool: True si le point est dans la base de données, False sinon
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select x, y from projet.point                          "
                    "   where x=%(x)s and y=%(y)s                           ",
                    {
                        "x": point[0],
                        "y": point[1]
                    },
                )
                res = cursor.fetchone()

        if res is not None:

            return True

        return False

    def get_point(self, id: int) -> Point:
        """
        Récupère un point de la base de données à partir de son identifiant

        Args:
            id (int): Identifiant unique du point dans la base de données

        Returns:
            Point: Objet représentant le point avec ses coordonnées (x, y),
            None si le point n'existe pas
        """
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
        """
        Récupère l'identifiant d'un point dans la base de données à partir
         de ses coordonnées

        Args:
            point (tuple): Coordonnées du point sous la forme (x, y)

        Returns:
            int: Identifiant unique du point dans la base de données,
            None si le point n'existe pas
        """

        id = None

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select id_point from projet.point                    "
                    "   where x=%(x)s and y=%(y)s                         ",
                    {
                        "x": point[0],
                        "y": point[1]
                    },
                )
                res = cursor.fetchone()

        if res:

            id = res["id_point"]

        return id
