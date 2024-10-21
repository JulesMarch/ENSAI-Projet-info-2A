from utils.singleton import Singleton
from dao.db_connection import DBConnection


class DepartementDao(metaclass=Singleton):
    def find_by_code(self, niveau: str, code: int):
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
            f"Le numéro INSEE {res['code_insee']} correspond au"
            f"département {res['nom']} situé en"
            f"{res['niveau_superieur']}")
        return informations
