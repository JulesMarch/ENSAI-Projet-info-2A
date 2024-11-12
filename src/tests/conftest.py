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

    pytest.point_0 = Point(x=0, y=0)

    pytest.point_1 = Point(x=100, y=0)

    pytest.point_2 = Point(x=0, y=100)

    pytest.point_3 = Point(x=100, y=100)
