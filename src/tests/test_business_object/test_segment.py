import pytest


class TestSegment():

    def test_get_coef_directeur(self):

        # WHEN
        resultat_1 = pytest.segment_1.get_coef_directeur()
        resultat_2 = pytest.segment_2.get_coef_directeur()
        resultat_3 = pytest.diagonale_1.get_coef_directeur()

        # THEN
        assert resultat_1 == 1000000000
        assert resultat_2 == 0
        assert resultat_3 == 1

    def test_get_ordonnee_origine(self):

        # WHEN
        resultat_1 = pytest.segment_1.get_ordonnee_origine()
        resultat_2 = pytest.segment_2.get_ordonnee_origine()

        # THEN
        assert resultat_1 == 0
        assert resultat_2 == 100

    def test_detec_inters(self):

        # WHEN
        resultat_1 = pytest.diagonale_1.detec_inters(pytest.diagonale_2)
        resultat_2 = pytest.segment_1.detec_inters(pytest.segment_3)
        resultat_3 = pytest.segment_5.detec_inters(pytest.segment_3)

        # THEN
        assert resultat_1 is True
        assert resultat_2 is False
        assert resultat_3 is True
