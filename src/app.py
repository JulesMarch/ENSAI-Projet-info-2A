from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import List
from typing import Tuple
import uvicorn

from src.services.fonction_1 import find_by_code_insee, find_by_nom
from src.services.fonction_2 import find_by_coord


test = find_by_code_insee("11", "Région", 2023)
print(test)


# On instancie le webservice
app = FastAPI()


# Création d'un enpoint qui répond à la méthode GET à l'adresse "/" qui va
# retourner le message "Hello World"
@app.get("/")
async def root():
    return {"message": "Bienvenue sur notre API"}


# Gestionnaire d'exceptions global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Renvoyer un message standardisé en cas d'erreur
    return JSONResponse(
        status_code=500,
        content={
            "error": "Une erreur s'est produite",
            "detail": str(exc),
        },
    )


@app.get("/zonageparcode/{niveau}/{annee}/{code_insee}")
async def get_zone_par_code_insee(niveau, code_insee, annee: int):

    print(niveau, code_insee)
    answer = find_by_code_insee(str(code_insee), niveau, annee)
    return answer


@app.get("/zonageparnom/{niveau}/{annee}/{nom}")
async def get_zone_par_nom(niveau, nom, annee: int):
    print(niveau, nom)
    answer = find_by_nom(str(nom), niveau, annee)
    return answer


@app.get("/coordonees/{niveau}/2024/{longitude}/{latitude}")
async def find_coord(niveau: str, latitude: float, longitude: float):
    answer = find_by_coord(float(longitude), float(latitude), niveau)
    resultat_final = {
        "coordonées": (float(latitude), float(longitude)),
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

    return resultat_final


@app.post("/listepoints/")
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

        print("point trouvé !")
        dic_retour["Point " + str(i + 1)] = resultat_final
    return dic_retour

# Lancement de l'application sur le le port 80
if __name__ == "__main__":
    uvicorn.run(app, host="localhost")
