from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection

from src.dao.polygone_dao import PolygoneDao


class ComposanteConnexeDao(metaclass=Singleton):
    def add_composante_connexe(L: list, type_composante: str):
        """
        Add a polygone to the database
            (works only if the point is not already in the database)
        """

        # Remplissage des informations relatives à la composante connexe

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into projet.comp_connexe                "
                    "(type_composante) values (%(type_composante)s);",
                    {
                        'type_composante': type_composante
                    }
                )

        # Remplissage des informations relatives aux contours de la composante
        # On distingue deux cas

        if type_composante == 'Polygon':

            # il n'y a du'un seul contour dans la composante dans ce cas

            polygon = L[0]

            # Ajout du polygone

            PolygoneDao.add_polygone(polygon)

            # Remplissage de la table d'association polygone et composante con

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "insert into projet.association_connexe_polygone"
                        " (id_polygone, id_comp_connexe, ordre, creux)  "
                        "values                                         "
                        "((select max(id_polygone) from projet.polygone),"
                        "(select max(id_comp_connexe) from              "
                        "projet.comp_connexe), %(ordre)s, %(creux)s)    ",
                        {
                            'ordre': 0,
                            'creux': False
                        }
                    )

        elif type_composante == 'MultiPolygon':

            # Il y à plusieurs contours qui définissent la composante connexe

            for k in range(len(L)):

                list_polygon = L[k]

                if len(list_polygon) == 1:

                    # il n'y a du'un seul contour dans la composante dans ce cas

                    polygon = list_polygon[0]

                    # Ajout du polygone

                    PolygoneDao.add_polygone(polygon)

                    # Remplissage de la table d'association polygone et composante con

                    with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "insert into projet.association_connexe_polygone"
                                " (id_polygone, id_comp_connexe, ordre, creux)  "
                                "values                                         "
                                "((select max(id_polygone) from projet.polygone),"
                                "(select max(id_comp_connexe) from              "
                                "projet.comp_connexe), %(ordre)s, %(creux)s)    ",
                                {
                                    'ordre': 0,
                                    'creux': False
                                }
                            )

                else:

                    polygon = list_polygon[0]

                    PolygoneDao.add_polygone(polygon)

                    with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "insert into projet.association_connexe_polygone"
                                " (id_polygone, id_comp_connexe, ordre, creux)  "
                                "values                                         "
                                "((select max(id_polygone) from projet.polygone),"
                                "(select max(id_comp_connexe) from              "
                                "projet.comp_connexe), %(ordre)s, %(creux)s)    ",
                                {
                                    'ordre': k,
                                    'creux': False
                                }
                            )

                    list_creux = list_polygon.pop(0)

                    for k in range(len(list_creux)):

                        creux = L[k][0]

                        PolygoneDao.add_polygone(creux)

                        with DBConnection().connection as connection:
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "insert into projet.association_connexe_polygone"
                                    " (id_polygone, id_comp_connexe, ordre, creux)  "
                                    "values                                         "
                                    "((select max(id_polygone) from projet.polygone),"
                                    "(select max(id_comp_connexe) from              "
                                    "projet.comp_connexe), %(ordre)s, %(creux)s)    ",
                                    {
                                        'ordre': 11,
                                        'creux': True
                                    }
                                )

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into projet.asso_zone_comp_co           "
                    " (id_zone, id_comp_connexe) values             "
                    "((select max(id_zone) from projet.zone_geo),   "
                    "(select max(id_comp_connexe) from              "
                    "projet.comp_connexe))                          "
                )
