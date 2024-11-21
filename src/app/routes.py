from fastapi import APIRouter, Query
from typing import List, Tuple
from app.auth import signup, login  # Authentification
from src.services.fonction_1 import find_by_code_insee, find_by_nom
from src.services.fonction_2 import find_by_coord
from app.utils import Conversion


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Bienvenue sur notre API"}

@router.post("/signup")
async def user_signup(username: str, password: str):
    return signup(username, password)

@router.post("/login")
async def user_login(username: str, password: str):
    return login(username, password)

@router.get("/zonageparcode/{niveau}/2024/{code_insee}")
async def get_zone_par_code_insee(niveau, code_insee):
    return find_by_code_insee(str(code_insee), niveau)

@router.get("/zonageparnom/{niveau}/2024/{nom}")
async def get_zone_par_nom(niveau, nom):
    return find_by_nom(str(nom), niveau)

@router.get("/coordonees/{niveau}")
async def find_coord(
    niveau: str,
    lat: float = Query(..., description="Latitude du point"),
    long: float = Query(..., description="Longitude du point"),
    type_coord: str = "GPS",
):
    if type_coord == "Lambert":
        long, lat = Conversion.lambert93_into_gps(long, lat)
    return find_by_coord(long, lat, niveau)

@router.post("/listepoints/")
async def find_points_loc(points: List[Tuple[float, float, str]]):
    results = {}
    for i, point in enumerate(points):
        long, lat, niveau = point
        result = find_by_coord(long, lat, niveau)
        results[f"Point {i+1}"] = result
    return results


