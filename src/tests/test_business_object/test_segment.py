import pytest
from src.business_object.segment import Segment
from src.business_object.point import Point


class TestSegment():

    def test_get_coef_directeur(self):

        # GIVEN
        x1, y1 = 1, 2
        x2, y2 = 1, 4
        x3, y3 = 2, 4
        S1 = Segment(Point(x1, y1), Point(x2, y2))
        S2 = Segment(Point(x1, y1), Point(x3, y3))

        segment_3 = Segment(pytest.point_0, pytest.point_2)

        # WHEN
        resultat1 = S1.get_coef_directeur()
        resultat2 = S2.get_coef_directeur()
        resultat3 = segment_3.get_coef_directeur()

        # THEN
        assert resultat1 is None
        assert resultat2 == 2
        assert resultat3 is None
