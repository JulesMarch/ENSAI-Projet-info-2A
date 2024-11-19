from src.business_object.point import Point
import pytest


# Point

@pytest.fixture
def point_0_kwargs():
    return dict(x=0, y=0)


def point_1_kwargs():
    return dict(x=100, y=0)


def point_2_kwargs():
    return dict(x=0, y=100)


def point_3_kwargs():
    return dict(x=100, y=100)


# Configuration globale

def pytest_configure():

    # Point

    pytest.tour_eiffel = Point(x=2.29448, y=40.1316)

    pytest.ensae = Point(x=2.2076, y=48.7110)

    pytest.mont_st_michel = Point(x=1.5115, y=48.6361)

    pytest.point_3 = Point(x=100, y=100)
