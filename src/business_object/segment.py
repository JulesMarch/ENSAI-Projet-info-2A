from src.business_object.point import Point


class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def get_coef_directeur(self) -> float:

        # Si la droite est verticale, il n'y a pas de coefficient directeur
        if self.p1.x == self.p2.x:
            return 1000000000
        return (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)

    def get_ordonnee_origine(self) -> float:
        a = self.get_coef_directeur()
        return self.p1.y - a*self.p1.x

    def detec_inters(self, seg) -> bool:

        # On récupère les paramètres des droites qui portent les segments
        a1, b1 = self.get_coef_directeur(), self.get_ordonnee_origine()
        a2, b2 = seg.get_coef_directeur(), seg.get_ordonnee_origine()

        # On regarde d'abord si les droites se coupent
        if a1 == a2:
            if b1 == b2:
                # Les droites sont confondues
                return False
            else:
                # Les droites sont parallèles
                return False

        else:
            # On calcule le point d'intersection entre les deux droites
            x = (b2-b1) / (a1-a2)
            y = a1*x+b1

        # Bornes des intervalles d'acceptation
        x_min_self, x_max_self = min(self.p1.x, self.p2.x),
        max(self.p1.x, self.p2.x)
        y_min_self, y_max_self = min(self.p1.y, self.p2.y),
        max(self.p1.y, self.p2.y)
        x_min_seg, x_max_seg = min(seg.p1.x, seg.p2.x), max(seg.p1.x, seg.p2.x)
        y_min_seg, y_max_seg = min(seg.p1.y, seg.p2.y), max(seg.p1.y, seg.p2.y)

        if (
            x_min_self <= x <= x_max_self and y_min_self <= y <= y_max_self and
            x_min_seg <= x <= x_max_seg and y_min_seg <= y <= y_max_seg
        ):
            return True

        return False
