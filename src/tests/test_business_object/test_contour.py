import pytest


class TestContour:
    def test_comptage_inters(self):

        # WHEN
        resultat_1 = pytest.contour.comptage_inters(pytest.segment_5)

        # THEN
        assert resultat_1 == 1
