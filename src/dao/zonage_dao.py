from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection

from src.business_object.point import Point


class ZonageDao(metaclass=Singleton):
    def add_zone_geo()


    def find_by_nom(nom: str):
        """
        Find a zonage in the database using the name and the geographic level
        """

        zone_geo = None

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where nom=%(nom)s                                 ",
                    {
                        "nom": nom
                    },
                )
                res = cursor.fetchone()

        if res: 


            
    def find_by_code_insee(code_insee: str):
        """
        Find a zonage in the database using the name and the geographic level
        """

        zone_geo = None

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where code_insee=%(code_insee)s                   ",
                    {
                        "code_insee": code_insee
                    },
                )
                res = cursor.fetchone()

        if res: 
            
