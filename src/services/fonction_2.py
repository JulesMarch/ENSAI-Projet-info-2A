# Cas pour région
from src.business_object.point import Point
# from src.business_object.departement import Departement
from src.dao.region_dao import RegionDao
from src.dao.departement_dao import DepartementDao
from src.dao.commune_dao import CommuneDao
from src.dao.arrondissement_dao import ArrondissementDao
from src.dao.IRIS_dao import IrisDao

niveaux_possibles = [
    "Région", "Département", "Commune", "IRIS", "Arrondissement"]


def find_by_coord(longitude: float, latitude: float, niveau: str):
    """
    Recherche un zonage basé sur les coordonnées géographiques
     (longitude, latitude) et le niveau spécifié

    Args:
        longitude (float): La longitude de la position à rechercher
        latitude (float): La latitude de la position à rechercher
        niveau (str): Le niveau géographique

    Returns:
        dict: Dictionnaire contenant les informations de la zone correspondant
        aux coordonnées fournies

    Raise:
        ValueError: Si le niveau fourni n'est pas valide
    """

    if niveau not in niveaux_possibles:
        raise ValueError(f'Le niveau doit être dans {niveaux_possibles}')

    if niveau == "Région":
        return find_region(longitude, latitude)

    elif niveau == "Département":
        return find_departement(longitude, latitude)

    elif niveau == "Commune":
        return find_commune(longitude, latitude)

    elif niveau == "Arrondissement":
        return find_arrondissement(longitude, latitude)

    elif niveau == "Iris":
        return find_iris(longitude, latitude)


def find_region(x: float, y: float):
    """
    Recherche une région en fonction des coordonnées géographiques (x, y)

    Args:
        x (float): La longitude du point à vérifier
        y (float): La latitude du point à vérifier

    Returns:
        Region: L'objet région correspondant au point si le point appartient
         à une région

    Raise:
        ValueError: Si le point n'est pas situé en France
        (n'appartient à aucune région)
    """
    pt_depart = Point(x=x, y=y)

    lst_reg = RegionDao.get_all_regions()
    for reg in lst_reg:
        curr_reg = RegionDao.construction_region(reg)
        if curr_reg.appartient_zonage(pt_depart):
            return curr_reg
    raise ValueError("Ce point n'est pas situé en France")


# cas pour departement

def find_departement(x: float, y: float):
    """
    Recherche un département en fonction des coordonnées géographiques (x, y)

    Args:
        x (float): La longitude du point à vérifier
        y (float): La latitude du point à vérifier

    Returns:
        Region: L'objet département correspondant au point si le point
        appartient à un département

    Raise:
        ValueError: Si le point n'est pas situé en France
        (n'appartient à aucun département)
    """
    pt_depart = Point(x=x, y=y)

    reg = find_region(x, y)

    lst_dep = DepartementDao.get_all_dep_in(reg.num_rgn)
    for dep in lst_dep:
        curr_dep = DepartementDao.construction_departement(dep)
        if curr_dep.appartient_zonage(pt_depart):
            return (curr_dep, reg)
    raise ValueError("Ce point n'est pas situé en France")


# cas pour commune

def find_commune(x: float, y: float):
    """
    Recherche une commune en fonction des coordonnées géographiques (x, y)

    Args:
        x (float): La longitude du point à vérifier
        y (float): La latitude du point à vérifier

    Returns:
        tuple: Tuple contenant les objets Commune et Département
        correspondants si le point appartient à une commune

    Raise:
        ValueError: Si le point n'est pas situé en France ou n'appartient
         à aucune commune
    """
    pt_depart = Point(x=x, y=y)

    dep = find_departement(x, y)[0]

    lst_com = CommuneDao.get_all_com_in(dep.num_dep)
    for com in lst_com:
        curr_com = CommuneDao.construction_commune(com)
        if curr_com.appartient_zonage(pt_depart):
            return (curr_com, dep)
    raise ValueError("Ce point n'est pas situé en France")


# cas pour les arrondissements

def find_arrondissement(x: float, y: float):
    """
    Recherche un arrondissement en fonction des coordonnées géographiques
     (x, y)

    Args:
        x (float): La longitude du point à vérifier
        y (float): La latitude du point à vérifier

    Returns:
        tuple: Tuple contenant les objets Arrondissement et Commune
        correspondants si le point appartient à un arrondissement

    Raise:
        ValueError: Si le point n'est pas situé en France ou n'appartient
         à aucun arrondissement
    """
    pt_depart = Point(x=x, y=y)

    com = find_commune(x, y)[0]

    lst_arr = ArrondissementDao.get_all_arr_in(com.code_postal)
    for arr in lst_arr:
        curr_arr = ArrondissementDao.construction_arrondissement(arr)
        if curr_arr.appartient_zonage(pt_depart):
            return (curr_arr, com)
    raise ValueError("Ce point n'est pas situé en France")


# cas pour les IRIS

def find_iris(x: float, y: float):
    """
    Recherche un arrondissement en fonction des coordonnées géographiques
     (x, y)

    Args:
        x (float): La longitude du point à vérifier
        y (float): La latitude du point à vérifier

    Returns:
        tuple: Tuple contenant les objets Arrondissement et Commune
        correspondants si le point appartient à un arrondissement

    Raise:
        ValueError: Si le point n'est pas situé en France ou n'appartient
         à aucun arrondissement
    """
    pt_depart = Point(x=x, y=y)

    com = find_commune(x, y)[0]

    lst_iris = IrisDao.get_all_iris_in(com.code_postal)
    for iris in lst_iris:
        curr_iris = IrisDao.construction_IRIS(iris)
        if curr_iris.appartient_zonage(pt_depart):
            return (curr_iris, com)
    raise ValueError("Ce point n'est pas situé en France")

# testTE = find_arrondissement(2.2945006, 48.8582599)[0].nom
# print("Tour eiffel :", testTE)

# testDunk = find_region(2.3772525, 51.0347708).nom
# print("Dunkerque :", testDunk)

# testStrasb = find_region(7.750589152096361, 48.581766559651534).nom
# print("Strasbourg : ", testStrasb)

# testENSAI = find_departement(-1.7420038, 48.0511495).nom
# print("L'ENSAI : ", testENSAI)

# testMailis = find_departement(-3.57675, 47.90345).nom
# print("Mailis habite en ", testMailis)

# testrand = find_region(-0.9848975978939434, 48.998783121883186).nom
# print("Ville dans la Manche au pif :", testrand)

# testBdx = find_region(-0.5787921, 44.8228784).nom
# print("Bordeaux :", testBdx)

# test_Bez = find_region(3.2131307, 43.3426562).nom
# print("Béziers :", test_Bez)

# testTls = find_region(1.4442469, 43.6044622).nom
# print("Toulouse :", testTls)

# testNantes = find_region(-1.4921233, 47.2971979).nom
# print("Carquefou :", testNantes)

# testIleNormande = find_region(-1.7967338631145924, 48.87806677986568).nom
# print("Aneret :", testIleNormande)

# testReux = find_by_coord(0.1522222, 49.2747222, "Commune")
# print("Reux :", testReux[0].nom)

# test_enclave = find_by_coord(4.967497754896986, 44.35637360344542, "Région")
# print(test_enclave[0].nom)
