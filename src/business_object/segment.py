from src.business_object.point import Point


class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def get_coef_directeur(self) -> float:

        # Si la droite est verticale, il n'y a pas de coefficient directeur
        if self.p1.x == self.p2.x:
            return 10000000000

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
        x_min = min(self.p1.x, self.p2.x)
        x_max = max(self.p1.x, self.p2.x)
        y_min = min(self.p1.y, self.p2.y)
        y_max = max(self.p1.y, self.p2.y)

        # On teste si le point d'intersection est dans l'intervalle
        if x_min <= x and x <= x_max:
            if y_min <= y and y <= y_max:
                # print([[x,y],([seg.p1.x, seg.p1.y], [seg.p2.x, seg.p2.y]), ([self.p1.x, self.p1.y], [self.p2.x, self.p2.y])])
                return True

        return False
