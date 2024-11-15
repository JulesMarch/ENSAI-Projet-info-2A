from utils.singleton import Singleton
from dao.db_connection import DBConnection


class ArrondissementDao(metaclass=Singleton):
    def find_by_code(self, niveau: str, code: int):
        """
        Recherche des informations sur un arrondissement à partir de son code INSEE
        
        Args:
            niveau (str): Niveau géographique (ex : "commune")
            code (int): Code INSEE de la zone à rechercher

        Returns:
            str: Informations sur l'arrondissement, incluant le code INSEE, 
                 le nom de la commune et la zone supérieure.
        """

        request = (
            f"SELECT code_insee, nom, zone_superieur"
            f"FROM projet.zone_geo"
            f"WHERE code_insee = {code}"
        )

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(request)
                res = cursor.fetchone()

        informations = (
            f"Le code {res['code_insee']} correspond à l'arrondissement"
            f"commune {res['nom']} situé en {res['niveau_superieur']}")
        return informations
