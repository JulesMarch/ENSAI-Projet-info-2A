from src.utils.singleton import Singleton
from src.business_object.point import Point
from src.business_object.segment import Segment
from src.business_object.contour import Contour
from src.business_object.region import Region
from src.dao.db_connection import DBConnection


class RegionDao(metaclass=Singleton):
    def add_region(zone: dict):
        """
        Add a Region to the database
            (works only if the region is not already in the database)
        """

        # if not ZonageDao.est_dans(zone):

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into projet.zone_geo (nom, niveau,          "
                    " code_insee, niveau_superieur) VALUES              "
                    " (%(nom)s, %(niveau)s,                             "
                    " %(code_insee)s, %(niveau_superieur)s)             ",
                    {
                        "nom": zone["NOM"],
                        "niveau": "Région",
                        "code_insee": zone["INSEE_REG"],
                        "niveau_superieur": "Null"
                    },
                )

    def find_by_code_insee(code_insee: str):
        """
        Find a zonage in the database using the name and the geographic level
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                          "
                    " where code_insee=%(code_insee)s                       ",
                    {
                        "code_insee": code_insee
                    },
                )
                res = cursor.fetchone()

        resultat_final = None

        if res:

            resultat_final = {
                "nom": res["nom"],
                "niveau": res["niveau"],
                "code_insee": res["code_insee"],
            }

            return resultat_final

        raise ValueError(
                "Le code donné n'est associé à aucune Région."
            )

    def find_region(x: float, y: float):

        pt_depart = Point(x=x, y=y)

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.zone_geo                      "
                    " where niveau= 'Région'           ",
                )
                res = cursor.fetchall()

        for reg in res:

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
                            "code_insee": reg["code_insee"]
                        }
                    )
                    pts_perim = cursor.fetchall()

                print(reg["nom"])
                print("total : ", len(pts_perim))
                lst_pts_perim = []
                lst_pts_creux =[]
                for pt in pts_perim:
                    if not pt["creux"] :
                        #print(pt["creux"])
                        lst_pts_perim.append(Point(pt["x"], pt["y"]))
                    else :
                        # print(pt["id_polygone"])
                        lst_pts_creux.append([Point(pt["x"], pt["y"]), pt["id_polygone"]])
                print("sans creux : ", len(lst_pts_perim))
                print("creux : ", len(lst_pts_creux))

                print("Etape 1 réussie")

                #Très long, Dieu sait pourquoi

                lst_poly_creux = []
                lst_id_poly = []
                if len(lst_pts_creux) > 0:
                    for i in range(0, max(k[1] for k in lst_pts_creux)):
                        temp_lst = []
                        for j in lst_pts_creux:
                            if i == j[1]:
                                temp_lst.append(j[0])
                        lst_poly_creux.append(temp_lst)

                print("Etape 2 réussie")

                lst_seg_perim = []
                for i in range(0, len(lst_pts_perim)-1):
                    lst_seg_perim.append(Segment(lst_pts_perim[i], lst_pts_perim[i+1]))
                lst_seg_perim.append(Segment(lst_pts_perim[len(lst_pts_perim) - 1], lst_pts_perim[0]))
                # print(len(lst_seg))

                lst_contours_creux =[]
                for poly in lst_poly_creux:
                    if len(poly) > 0:
                        lst_seg_temp = []
                        # print(len(poly))
                        for i in range(0, len(poly)-1):
                            lst_seg_temp.append(Segment(poly[i], poly[i+1]))
                        lst_seg_temp.append(Segment(poly[len(poly) - 1], poly[0]))
                        lst_contours_creux.append(Contour(lst_seg_temp))

                print("Etape 3 réussie")

            curr_reg = Region(
                nom=reg["nom"],
                num_rgn=reg["code_insee"],
                perimetre=Contour(lst_seg_perim),
                creux=lst_contours_creux,
                edition_carte="2024"
            )

            if curr_reg.appartient_zonage(pt_depart):
                return curr_reg
        raise ValueError("Ce point n'est pas situé en France")


# testTE = RegionDao.find_region(2.2945006, 48.8582599).nom
# print("Tour eiffel :", testTE)

# testDunk = RegionDao.find_region(2.3772525, 51.0347708).nom
# print("Dunkerque :", testDunk)

# testStrasb = RegionDao.find_region(7.750589152096361, 48.581766559651534).nom
# print("Strasbourg : ", testStrasb)

# testMailis = RegionDao.find_region(-3.57675, 47.90345).nom
# print("Mailis habite en ", testMailis)

# testENSAI = RegionDao.find_region(-1.7420038, 48.0511495).nom
# print("L'ENSAI : ", testENSAI)

# testrand = RegionDao.find_region(-0.9848975978939434, 48.998783121883186).nom
# print("Ville dans la Manche au pif :", testrand)

# testBdx = RegionDao.find_region(-0.5787921, 44.8228784).nom
# print("Bordeaux :", testBdx)

# test_Bez = RegionDao.find_region(3.2131307, 43.3426562).nom
# print("Béziers :", test_Bez)
