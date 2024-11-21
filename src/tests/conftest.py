import pytest

from src.business_object.point import Point
from src.business_object.segment import Segment
from src.business_object.contour import Contour


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

    pytest.tour_eiffel = Point(x=2.2945006, y=48.8582599)

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
