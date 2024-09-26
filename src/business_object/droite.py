from src.business_object.point import Point


class Droite:
    def __init__(self, p1: Point, p2: Point):

        self.p1 = p1
        self.p2 = p2

    def get_coef_direct(self):
        return (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)

    def get_origine(self):
        a = self.get_coef_direct()
        return self.p1.y - a*self.p1.x


def intersection(D1: Droite, D2: Droite):

    # On récupère les paramètres respectifs des droites
    a1, b1 = D1.get_coef_direct(), D1.get_origine()
    a2, b2 = D2.get_coef_direct(), D2.get_origine()

    if a1 == a2:
        if b1 == b2:
            # Les droites sont confondues
            return "nique sa mère ya trop de solutions"
        else:
            # Les droites sont parallèles
            return "nique sa mère ya pas de solutions"

    else:
        x = (b2-b1) / (a1-a2)
        y = a1*x+b1

    return x, y
