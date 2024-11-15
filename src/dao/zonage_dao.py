from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection

from src.business_object.point import Point
from src.business_object.zonage import Zonage
from src.dao.contour_dao import ContourDao
# from src.dao.region_dao import RegionDao
# from src.dao.departement_dao import DepartementDao
# from src.dao.commune_dao import CommuneDao

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
                    "select * from projet.zone_geo                       "
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

        if niveau == "Région":
            return RegionDao.find_by_nom(nom)

        elif niveau == "Département":
            return DepartementDao.find_by_nom(nom)

        elif niveau == "Commune":
            return CommuneDao.find_by_nom(nom)

    # def find_by_code_insee(code_insee: str, niveau: str):
    #     """
    #     Find a zonage in the database using the name and the geographic level
    #     """
    #     if niveau not in niveaux:
    #         raise ValueError('le niveau doit être un des suivants: "region",' +
    #                          '"departement", "commune", "arrondissement",' +
    #                          '"IRIS"')

    #     if niveau == "Région":
    #         return RegionDao.find_by_code_insee(code_insee)

    #     elif niveau == "Département":
    #         return DepartementDao.find_by_code_insee(code_insee)

    #     elif niveau == "Commune":
    #         return CommuneDao.find_by_code_insee(code_insee)

    def construction_zonage(zone):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT x, y, creux, id_polygone FROM projet.point "
                    "JOIN projet.association_polygone_point USING (id_point) "
                    "JOIN projet.polygone USING (id_polygone) "
                    "JOIN projet.association_connexe_polygone USING (id_polygone)"
                    "JOIN projet.comp_connexe USING (id_comp_connexe)"
                    "JOIN projet.asso_zone_comp_co USING (id_comp_connexe)"
                    "JOIN projet.zone_geo USING (id_zone) "
                    "where projet.zone_geo.code_insee =%(code_insee)s"
                    "ORDER BY projet.association_polygone_point.ordre ASC",
                    {
                        "code_insee": zone["code_insee"]
                    }
                )
                pts_perim = cursor.fetchall()

            print(zone["nom"])
            print("total : ", len(pts_perim))
            lst_pts_perim = []
            lst_pts_creux = []
            for pt in pts_perim:
                if not pt["creux"]:
                    # print(pt["creux"])
                    lst_pts_perim.append(Point(pt["x"], pt["y"]))
                else:
                    # print(pt["id_polygone"])
                    lst_pts_creux.append([Point(pt["x"], pt["y"]),
                                         pt["id_polygone"]])
            print("sans creux : ", len(lst_pts_perim))
            print("creux : ", len(lst_pts_creux))

            print("Etape 1 réussie")

            # Très long, Dieu sait pourquoi

            lst_poly_creux = []
            if len(lst_pts_creux) > 0:
                for i in range(0, max(k[1] for k in lst_pts_creux)):
                    temp_lst = []
                    for j in range(len(lst_pts_creux)):
                        if i == lst_pts_creux[j][1]:
                            pt = lst_pts_creux.pop(j)
                            temp_lst.append(pt[0])
                    lst_poly_creux.append(temp_lst)

            print("Etape 2 réussie")

            lst_seg_perim = ContourDao.construction_contour(lst_pts_perim)

            lst_contours_creux = []
            for poly in lst_poly_creux:
                if len(poly) > 0:
                    temp_cont = ContourDao.construction_contour(poly)
                    lst_contours_creux.append(temp_cont)

            print("Etape 3 réussie")

        zone = Zonage(
            nom=zone["nom"],
            perimetre=lst_seg_perim,
            creux=lst_contours_creux,
            edition_carte="2024"
        )

        return zone
