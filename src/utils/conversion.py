from pyproj import Transformer

from src.business_object.point import Point


class Conversion:
    def lamber93_into_gps(point: Point):

        # Définition du transformateur
        transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326")

        longitude, latitude = transformer.transform(
            point.x, point.y
        )

        return longitude, latitude
