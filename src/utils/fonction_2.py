# Cas pour région
from src.business_object.point import Point
# from src.business_object.departement import Departement
from src.dao.region_dao import RegionDao


def find_region(x: float, y: float):

    pt_depart = Point(x=x, y=y)

    lst_reg = RegionDao.get_all_regions()
    for reg in lst_reg:
        curr_reg = RegionDao.construction_region(reg)
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


# testTE = find_region(2.2945006, 48.8582599).nom
# print("Tour eiffel :", testTE)

# testDunk = find_region(2.3772525, 51.0347708).nom
# print("Dunkerque :", testDunk)

# testStrasb = find_region(7.750589152096361, 48.581766559651534).nom
# print("Strasbourg : ", testStrasb)

# testENSAI = find_region(-1.7420038, 48.0511495).nom
# print("L'ENSAI : ", testENSAI)

# testMailis = find_region(-3.57675, 47.90345).nom
# print("Mailis habite en ", testMailis)

# testrand = find_region(-0.9848975978939434, 48.998783121883186).nom
# print("Ville dans la Manche au pif :", testrand)

# testBdx = find_region(-0.5787921, 44.8228784).nom
# print("Bordeaux :", testBdx)

# test_Bez = find_region(3.2131307, 43.3426562).nom
# print("Béziers :", test_Bez)

# testTls = find_region(1.4442469, 43.6044622).nom
# print("Toulouse :", testTls)
