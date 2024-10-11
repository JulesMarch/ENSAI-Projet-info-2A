from src.business_object.segment import Segment


class Contour:
    def __init__(self, L: list(Segment)):
        self.lst_segments = L

    def comptage_inters(self, DD: Segment) -> int:
        nb_inters = 0
        for seg in self.lst_segments:
            if DD.detec_inters(seg):
                nb_inters += 1
        return nb_inters
