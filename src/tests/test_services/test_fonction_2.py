import pytest

import src.services.fonction_2 as F2


class TestFonction2():
    def test_find_region(self):

        # GIVEN
        x = pytest.tour_eiffel.x
        y = pytest.tour_eiffel.y

        # WHEN
        resultat = F2.find_region(x, y)

        # THEN
        assert resultat.nom == "Île-de-France"

    def test_find_departement(self):

        # GIVEN
        x = pytest.tour_eiffel.x
        y = pytest.tour_eiffel.y

        # WHEN
        resultat = F2.find_departement(x, y)

        # THEN
        assert resultat[0].nom == "Paris"

    def test_find_commune(self):

        # GIVEN
        x = pytest.tour_eiffel.x
        y = pytest.tour_eiffel.y

        # WHEN
        resultat = F2.find_departement(x, y)

        # THEN
        assert resultat[0].nom == "Paris"