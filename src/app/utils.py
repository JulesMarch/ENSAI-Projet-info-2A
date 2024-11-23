from passlib.context import CryptContext
from pyproj import Transformer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class Conversion:
    def lambert93_into_gps(x, y):

        # Définition du transformateur
        transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326")

        longitude, latitude = transformer.transform(
            x, y
        )

        return longitude, latitude
