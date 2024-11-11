# Cas pour région
from src.business_object.point import Point
from src.business_object.segment import Segment
from src.business_object.contour import Contour
from src.business_object.region import Region
# from src.business_object.departement import Departement
from src.dao.db_connection import DBConnection


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
                    "SELECT x, y FROM projet.point "
                    "JOIN projet.association_polygone_point USING (id_point) "
                    "JOIN projet.polygone USING (id_polygone) "
                    "JOIN projet.zone_geo ON projet.zone_geo.id_zone = projet.polygone.id_polygone "
                    "where projet.zone_geo.code_insee =%(code_insee)s ",
                    {
                        "code_insee": reg["code_insee"]
                    }
                )
                pts_perim = cursor.fetchall()

        lst_pts_perim = []
        for pt in pts_perim:
            lst_pts_perim.append(Point(pt["x"], pt["y"]))
        # print(len(lst_pts_perim))

        lst_seg = []
        for i in range(0, len(lst_pts_perim)-1):
            lst_seg.append(Segment(lst_pts_perim[i], lst_pts_perim[i+1]))
        lst_seg.append(Segment(lst_pts_perim[len(lst_pts_perim) -1], lst_pts_perim[0]))
        # print(len(lst_seg))

        curr_reg = Region(
            nom=reg["nom"],
            num_rgn=reg["code_insee"],
            perimetre=Contour(lst_seg),
            creux="tbd",
            edition_carte="2024"
        )

        print(curr_reg.nom)

        if curr_reg.appartient_zonage(pt_depart):
            return curr_reg
    raise ValueError("Ce point n'est pas situé en France")

# cas pour departement


# def find_departement(x: float, y: float):
#     reg = find_region(x, y)
#     pt_depart = Point(x=x, y=y)

#     with DBConnection().connection as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "select * from projet.zone_geo                      "
#                 " where niveau= Département AND niveau_supérieur =", reg
#             )
#             res = cursor.fetchall()

#     for dep in res:
#         curr_dep = Departement(
#             nom=dep["NOM"],
#             num_rgn=dep["CODE_INSEE"],
#             perimetre="tbd",
#             creux="tbd",
#             edition_carte="2024"
#         )

#         if curr_dep.appartient_zonage(pt_depart):
#             print("Ce point se trouve en ", + curr_dep.nom)
#             return curr_dep.num_rgn

# # cas pour commune


# def find_commune(x: float, y: float):
#     dep = find_departement(x, y)
#     pt_depart = Point(x=x, y=y)

#     with DBConnection().connection as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "select * from projet.zone_geo                      "
#                 " where niveau= Commune AND niveau_supérieur =", dep
#             )
#             res = cursor.fetchall()

#     for com in res:
#         curr_com = Departement(
#             nom=com["NOM"],
#             num_rgn=com["CODE_INSEE"],
#             perimetre="tbd",
#             creux="tbd",
#             edition_carte="2024"
#         )

#         if curr_com.appartient_zonage(pt_depart):
#             print("Ce point se trouve en ", + curr_com.nom)
#             return curr_com.num_rgn


testTE = find_region(2.2945006, 48.8582599).nom
print("Tour eiffel :", testTE)

testDunk = find_region(2.3772525, 51.0347708).nom
print("Dunkerque :", testDunk)

testStrasb = find_region(7.750589152096361, 48.581766559651534).nom
print("Strasbourg : ", testStrasb)

testrand = find_region(-0.9848975978939434, 48.998783121883186).nom
print("Ville dans la Manche au pif :", testrand)
