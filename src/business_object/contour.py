from src.business_object.segment import Segment

class Contour:
    def __init__(self, L: list(Segment)):
        self.L = L
        for i in range(len(L)):
            Segment_i = Segment(L[i])
    

    def nbre_intersection(self, )