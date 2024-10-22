from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection


niveaux = ["Région", "Département", "Commune", "Arrondissement", "IRIS"]


class ZonageDao(metaclass=Singleton):
    def add_zone_geo(zone: dict):
        """
        Add a geographical zone to the database
            (works only if the zone is not already in the database)
        """

        # if not ZonageDao.est_dans(zone):

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DO $$                                              "
                    "BEGIN                                              "
                    "   IF NOT EXISTS (SELECT 1 FROM pg_class           "
                    "WHERE relname = 'seq_id_zone_geo') THEN"
                    "   EXECUTE 'CREATE SEQUENCE seq_id_zone_geo';      "
                    "   END IF;                                         "
                    "END $$;                                            "

                    "INSERT INTO projet.zone_geo (id_zone, nom, niveau, "
                    " code_insee, niveau_superieur) VALUES              "
                    " (nextval('seq_id_zone_geo'), %(nom)s, %(niveau)s, "
                    " %(code_insee)s, %(niveau_superieur)s)             ",
                    {
                        "nom": zone["NOM"],
                        "niveau": "Région",
                        "code_insee": zone["INSEE_REG"],
                        "niveau_superieur": "Null"
                    },
                )

    def est_dans(zone: dict) -> bool:
        """
        Tell if a geographical zone is in the database
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.point                          "
                    "   where nom, niveau, code_insee                    ",
                    {
                        "nom": zone["NOM"],
                        "y": point[1],
                    },
                )
                res = cursor.fetchone()

        if res:

            return True

        return False

    def find_by_nom(nom: str, niveau: str):
        """
        Find a zonage in the database using the name and the geographic level
        """

        if niveau not in niveaux:
            raise ValueError('le niveau doit être un des suivants: "region",' +
                             '"departement", "commune", "arrondissement",' +
                             '"IRIS"')

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where nom=%(nom)s and niveau=%(niveau)s           ",
                    {
                        "nom": nom,
                        "niveau": niveau
                    },
                )
                res = cursor.fetchall()

        resultat_final = []
        for row in res:
            infos = {
                "nom": row["nom"],
                "niveau": row["niveau"],
                "code_insee": row["code_insee"],
                "niveau_superieur": row["niveau_superieur"]
            }
            resultat_final.append(infos)

        return resultat_final

    def find_by_code_insee(code_insee: str, niveau: str):
        """
        Find a zonage in the database using the name and the geographic level
        """
        if niveau not in niveaux:
            raise ValueError('le niveau doit être un des suivants: "region",' +
                             '"departement", "commune", "arrondissement",' +
                             '"IRIS"')

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where code_insee=%(code_insee)s and niveau=%(niveau)s",
                    {
                        "code_insee": code_insee
                    },
                )
                res = cursor.fetchall()

        resultat_final = []
        for row in res:
            infos = {
                "nom": row["nom"],
                "niveau": row["niveau"],
                "code_insee": row["code_insee"],
                "niveau_superieur": row["niveau_superieur"]
            }
            resultat_final.append(infos)

        return resultat_final
