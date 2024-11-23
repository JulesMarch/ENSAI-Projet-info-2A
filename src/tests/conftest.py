import pytest

from src.business_object.point import Point
from src.business_object.segment import Segment
from src.business_object.contour import Contour


# Région

@pytest.fixture
def Region_Nouvelle_Aquitaine_kwargs():
    return {
        'nom': 'Nouvelle-Aquitaine',
        'niveau': 'Région',
        'code_insee': '75',
        'année': 2023
    }


@pytest.fixture
def Region_Grand_Est_kwargs():
    return {
        'nom': 'Grand Est',
        'niveau': 'Région',
        'code_insee': '44',
        'année': 2023
    }


# Département

@pytest.fixture
def Departement_Ille_et_Villaine_kwargs():
    return {
        'nom': 'Ille-et-Vilaine',
        'niveau': 'Département',
        'code_insee': '35',
        'Région': 'Bretagne',
        'année': 2023
    }


@pytest.fixture
def Departement_Ariege_kwargs():
    return {
        'nom': 'Ariège',
        'niveau': 'Département',
        'code_insee': '09',
        'Région': 'Occitanie',
        'année': 2023
    }


# Commune

@pytest.fixture
def Commune_Rennes_kwargs():
    return {
        'nom': 'Rennes',
        'niveau': 'Commune',
        'code_insee': '35238',
        'Département': 'Ille-et-Vilaine',
        'Région': 'Bretagne',
        'année': 2023
    }


@pytest.fixture
def Commune_Paris_kwargs():
    return {
        'nom': 'Paris',
        'niveau': 'Commune',
        'code_insee': '75056',
        'Département': 'Paris',
        'Région': 'Île-de-France',
        'année': 2023
    }


def point_2_kwargs():
    return dict(x=0, y=100)


def point_3_kwargs():
    return dict(x=100, y=100)


# Configuration globale

def pytest_configure():

    # Point

    pytest.origine = Point(x=0, y=0)

    pytest.point_100_0 = Point(x=100, y=0)

    pytest.point_0_100 = Point(x=0, y=100)

    pytest.point_100_100 = Point(x=100, y=100)

    pytest.point_50_50 = Point(x=50, y=50)

    pytest.point_150_50 = Point(x=150, y=50)

    # Segment

    pytest.segment_1 = Segment(
        pytest.origine, pytest.point_0_100
    )

    pytest.segment_2 = Segment(
        pytest.point_0_100, pytest.point_100_100
    )

    pytest.segment_3 = Segment(
        pytest.point_100_100, pytest.point_100_0
    )

    pytest.segment_4 = Segment(
        pytest.point_100_0, pytest.origine
    )

    pytest.segment_5 = Segment(
        pytest.point_50_50, pytest.point_150_50
    )

    pytest.diagonale_1 = Segment(
        pytest.origine, pytest.point_100_100
    )

    pytest.diagonale_2 = Segment(
        pytest.point_0_100, pytest.point_100_0
    )

    # Contour

    pytest.contour = Contour(
        list(
            (
                pytest.segment_1, pytest.segment_2,
                pytest.segment_3, pytest.segment_4
            )
        )
    )

    # Définition de points en France

    pytest.tour_eiffel = Point(x=2.2945006, y=48.8582599)

    pytest.ensae = Point(x=2.2079203, y=48.7109887)

    pytest.ensai = Point(x=-1.741779, y=48.050646)
