from abc import ABC
from src.business_object.segment import Segment
from src.business_object.point import Point


class Zonage(ABC):
    def __init__(
        self,
        nom: str,
        perimetre: list(Segment),
        creux: list(Segment),
        edition_carte: int
    ):

        self.nom = nom
        self.perimetre = perimetre
        self.creux = creux
        self.edition_carte = edition_carte

    def appartient_zonage(self, p):
        # Construction de la demi-droite
        p2 = Point(x=p.x, y=10000)
        DD = Segment(p, p2)
        # Détection du nb d'intersections
        nb_inters = 0
        nb_inters += self.perimetre.comptage_inters(DD)
        # Est-ce que le point appartient au zonage ?
        if nb_inters//2 == 1:
            for i in self.creux:
                nb_inters_creux = i.comptage_inters(DD)
                if nb_inters_creux//2 == 1:
                    return False
            return True
        else:
            return False
