from abc import ABC
from src.business_object.segment import Segment
from src.business_object.point import Point


class Zonage(ABC):
    def __init__(
        self,
        nom: str,
        perimetre: list[Segment],
        creux,
        edition_carte: int
    ):

        self.nom = nom
        self.perimetre = perimetre
        self.creux = creux
        self.edition_carte = edition_carte

    def appartient_zonage(self, p):
        # Construction de la demi-droite
        p2 = Point(x=180, y=p.y)
        DD = Segment(p, p2)
        # Détection du nb d'intersections
        nb_inters = 0
        for i in self.creux:
            nb_inters += i.comptage_inters(DD)
            # print(i.comptage_inters(DD))
        for j in self.perimetre:
            nb_inters += j.comptage_inters(DD)
            # print(j.comptage_inters(DD))
        # print(nb_inters)
        # Est-ce que le point appartient au zonage ?
        if nb_inters % 2 == 1:
            print("c'est bon !")
            return True
        else:
            print("échec...")
            return False
