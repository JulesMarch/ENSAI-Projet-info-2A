from pyproj import Transformer


class Conversion:
    def lambert93_into_gps(x, y):

        # Définition du transformateur
        transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326")

        longitude, latitude = transformer.transform(
            x, y
        )

        return longitude, latitude
