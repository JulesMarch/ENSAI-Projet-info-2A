from src.business_object.segment import Segment


class Contour:
    def __init__(self, L: list(Segment)):
        self.lst_segments = L

    def comptage_inters(self, D: Segment) -> int:
        pass
