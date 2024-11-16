from src.dao.region_dao import RegionDao
from src.dao.departement_dao import DepartementDao
from src.dao.commune_dao import CommuneDao


def find_by_code_insee(code_insee: str, niveau: str):
    """
    Find a zonage in the database using the name and the geographic level
    """

    if niveau == "Région":
        return RegionDao.find_by_code_insee(code_insee)

    elif niveau == "Département":
        return DepartementDao.find_by_code_insee(code_insee)

    elif niveau == "Commune":
        return CommuneDao.find_by_code_insee(code_insee)
