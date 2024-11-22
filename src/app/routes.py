from fastapi import APIRouter, Query
from typing import List, Tuple
from src.app.auth import signup, login  # Authentification
from src.services.fonction_1 import find_by_code_insee, find_by_nom
from src.services.fonction_2 import find_by_coord
from src.app.utils import Conversion


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Bienvenue sur notre API ! Nous vous invitons à "
            "aller sur http://localhost:8000/docs"}


# @router.post("/signup")
# async def user_signup(username: str, password: str):
#     return signup(username, password)


# @router.post("/login")
# async def login(username: str = Form(...), password: str = Form(...)):
#     print(f"Login attempt: username={username}, password={'*' * len(password)}")


@router.get("/zonageparcode/{niveau}/{annee}/{code_insee}")
async def get_zone_par_code_insee(niveau, code_insee, annee: int):
    print(niveau, code_insee)
    answer = find_by_code_insee(str(code_insee), niveau, annee)
    return answer


@router.get("/zonageparnom/{niveau}/{annee}/{nom}")
async def get_zone_par_nom(niveau, nom, annee: int):
    print(niveau, nom)
    answer = find_by_nom(str(nom), niveau, annee)
    return answer


@router.get("/coordonees/{niveau}")
async def find_coord(
    niveau: str,
    lat: float = Query(..., description="Latitude du point"),
    long: float = Query(..., description="Longitude du point"),
    annee: int = Query(..., description="Année de la recherche"),
    type_coord: str = "GPS"
        ):
    orig_lat, orig_long = lat, long
    if type_coord == "Lambert":
        orig_lat, orig_long = lat, long
        long, lat = Conversion.lambert93_into_gps(long, lat)
        print(long, lat)
    answer = find_by_coord(long, lat, niveau)
    resultat_final = {
        "coordonées": (orig_lat, orig_long),
        "niveau": niveau,
    }
    if niveau == "Région":
        resultat_final["nom"] = answer.nom
        resultat_final["code_insee"] = answer.num_rgn

    if niveau == "Département":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_dep
        resultat_final["région"] = answer[1].nom

    if niveau == "Commune":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].code_postal
        resultat_final["département"] = answer[1].nom

    if niveau == "Arrondissement":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_arr
        resultat_final["commune"] = answer[1].nom

    return resultat_final


@router.post("/listepoints/")
async def find_points_loc(points: List[Tuple[float, float, str]]):
    dic_retour = {}
    print(len(points))
    for i in range(0, len(points)):
        answer = find_by_coord(
            float(points[i][1]), float(points[i][0]), points[i][2])
        niveau = points[i][2]
        resultat_final = {}
        resultat_final = {
            "coordonées": (float(points[i][0]), float(points[i][1])),
            "niveau": niveau,
        }
        if niveau == "Région":
            resultat_final["nom"] = answer.nom
            resultat_final["code_insee"] = answer.num_rgn

        if niveau == "Département":
            resultat_final["nom"] = answer[0].nom
            resultat_final["code_insee"] = answer[0].num_dep
            resultat_final["région"] = answer[1].nom

        if niveau == "Commune":
            resultat_final["nom"] = answer[0].nom
            resultat_final["code_insee"] = answer[0].code_postal
            resultat_final["département"] = answer[1].nom

        if niveau == "Arrondissement":
            resultat_final["nom"] = answer[0].nom
            resultat_final["code_insee"] = answer[0].num_arr
            resultat_final["commune"] = answer[1].nom

        print("point trouvé !")
        dic_retour["Point " + str(i + 1)] = resultat_final
    return dic_retour
