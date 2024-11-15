from src.utils.singleton import Singleton
from src.business_object.contour import Contour
from src.business_object.segment import Segment


class ContourDao(metaclass=Singleton):
    def construction_contour(lst_pts):
        lst_seg = []
        for i in range(0, len(lst_pts)-1):
            lst_seg.append(Segment(lst_pts[i], lst_pts[i+1]))
        lst_seg.append(Segment(lst_pts[len(lst_pts) - 1], lst_pts[0]))
        return Contour(lst_seg)
