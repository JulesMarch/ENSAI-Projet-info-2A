from src.business_object.segment import Segment

class Contour:
    def __init__(self, L: list(Segment)):
        self.L = L

    def nbre_intersection(self, D: Segment) -> int:
        