import bcrypt
from pyproj import Transformer


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

class Conversion:
    def lambert93_into_gps(x, y):

        # Définition du transformateur
        transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326")

        longitude, latitude = transformer.transform(
            x, y
        )

        return longitude, latitude
