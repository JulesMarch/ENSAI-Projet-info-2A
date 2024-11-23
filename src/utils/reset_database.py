from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self):
        print("Ré-initialisation de la base de données")

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_as_string)
        except Exception as e:
            print(e)
            raise

        with open("data/pop_reg.py") as f:
            exec(f.read())

        with open("data/pop_dep.py") as f:
            exec(f.read())

        with open("data/pop_com.py") as f:
            exec(f.read())

        with open("data/pop_arr_municipal.py") as f:
            exec(f.read())

        with open("data/pop_iris.py") as f:
            exec(f.read())

        print("Ré-initialisation de la base de données - Terminée")

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
