from src.business_object.point import Point


class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def get_coef_direct(self):
        return (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)

    def get_origine(self):
        a = self.get_coef_direct()
        return self.p1.y - a*self.p1.x
