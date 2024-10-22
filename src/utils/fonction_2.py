# Cas pour région
from src.business_object.point import Point
from src.business_object.region import Region
from src.business_object.departement import Departement
from src.dao.db_connection import DBConnection


def find_region(x: float, y: float):
    pt_depart = Point(x=x, y=y)

    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from projet.zone_geo                      "
                " where niveau= Région           ",
            )
            res = cursor.fetchall()

    for reg in res:
        curr_reg = Region(
            nom=reg["NOM"],
            num_rgn=reg["CODE_INSEE"],
            perimetre="tbd",
            creux="tbd",
            edition_carte="2024"
        )

        if curr_reg.appartient_zonage(pt_depart):
            print("Ce point se trouve en ", + curr_reg.nom)
            return curr_reg.num_rgn
    raise ValueError("Ce point n'est pas situé en France")

# cas pour departement


def find_departement(x: float, y: float):
    reg = find_region(x, y)
    pt_depart = Point(x=x, y=y)

    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from projet.zone_geo                      "
                " where niveau= Département AND niveau_supérieur =", reg
            )
            res = cursor.fetchall()

    for dep in res:
        curr_dep = Departement(
            nom=dep["NOM"],
            num_rgn=dep["CODE_INSEE"],
            perimetre="tbd",
            creux="tbd",
            edition_carte="2024"
        )

        if curr_dep.appartient_zonage(pt_depart):
            print("Ce point se trouve en ", + curr_dep.nom)
            return curr_dep.num_rgn


def find_commune(x: float, y: float):
    dep = find_departement(x, y)
    pt_depart = Point(x=x, y=y)

    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from projet.zone_geo                      "
                " where niveau= Commune AND niveau_supérieur =", dep
            )
            res = cursor.fetchall()

    for com in res:
        curr_com = Departement(
            nom=com["NOM"],
            num_rgn=com["CODE_INSEE"],
            perimetre="tbd",
            creux="tbd",
            edition_carte="2024"
        )

        if curr_com.appartient_zonage(pt_depart):
            print("Ce point se trouve en ", + curr_com.nom)
            return curr_com.num_rgn
