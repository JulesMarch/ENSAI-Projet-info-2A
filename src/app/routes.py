from fastapi import APIRouter, Depends, Query
from typing import List, Tuple
from app.auth import get_current_user
from app.models import User
from src.services.fonction_1 import find_by_code_insee, find_by_nom
from src.services.fonction_2 import find_by_coord

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Bienvenue sur notre API ! Nous vous invitons à aller sur http://localhost:8000/docs"}

# @router.post("/login")
# async def login(username: str, password: str):
#     print(f"Login attempt: username={username}, password={'*' * len(password)}")

@router.get("/zonageparcode/{niveau}/{annee}/{code_insee}")
async def get_zone_par_code_insee(
    niveau: str, 
    code_insee: str, 
    annee: int,
    current_user: User = Depends(get_current_user)  # Protection par authentification
):
    print(f"Utilisateur authentifié : {current_user.username}")
    print(niveau, code_insee)
    answer = find_by_code_insee(str(code_insee), niveau, annee)
    return answer

@router.get("/zonageparnom/{niveau}/{annee}/{nom}")
async def get_zone_par_nom(
    niveau: str, 
    nom: str, 
    annee: int,
    current_user: User = Depends(get_current_user)  # Protection par authentification
):
    print(f"Utilisateur authentifié : {current_user.username}")
    print(niveau, nom)
    answer = find_by_nom(str(nom), niveau, annee)
    return answer

@router.get("/coordonees/{niveau}")
async def find_coord(
    niveau: str,
    lat: float = Query(..., description="Latitude du point"),
    long: float = Query(..., description="Longitude du point"),
    annee: int = Query(..., description="Année de la recherche"),
    type_coord: str = "GPS",
    current_user: User = Depends(get_current_user)  # Protection par authentification
):
    print(f"Utilisateur authentifié : {current_user.username}")
    answer = find_by_coord(long, lat, niveau)
    resultat_final = {
        "coordonées": (lat, long),
        "niveau": niveau,
    }
    if niveau == "Région":
        resultat_final["nom"] = answer.nom
        resultat_final["code_insee"] = answer.num_rgn
    elif niveau == "Département":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_dep
        resultat_final["région"] = answer[1].nom
    elif niveau == "Commune":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].code_postal
        resultat_final["département"] = answer[1].nom
    return resultat_final

@router.post("/listepoints/")
async def find_points_loc(
    points: List[Tuple[float, float, str]],
    current_user: User = Depends(get_current_user)  # Protection par authentification
):
    print(f"Utilisateur authentifié : {current_user.username}")
    dic_retour = {}
    for i, point in enumerate(points):
        try:
            answer = find_by_coord(float(point[1]), float(point[0]), point[2])
            niveau = point[2]
            resultat_final = {
                "coordonées": (float(point[0]), float(point[1])),
                "niveau": niveau,
            }
            if niveau == "Région":
                resultat_final["nom"] = answer.nom
                resultat_final["code_insee"] = answer.num_rgn
            elif niveau == "Département":
                resultat_final["nom"] = answer[0].nom
                resultat_final["code_insee"] = answer[0].num_dep
                resultat_final["région"] = answer[1].nom
            elif niveau == "Commune":
                resultat_final["nom"] = answer[0].nom
                resultat_final["code_insee"] = answer[0].code_postal
                resultat_final["département"] = answer[1].nom
            dic_retour[f"Point {i + 1}"] = resultat_final
        except Exception as e:
            dic_retour[f"Point {i + 1}"] = {"error": "Point introuvable", "detail": str(e)}
    return dic_retour