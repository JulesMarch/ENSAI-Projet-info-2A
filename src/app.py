from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from src.services.fonction_1 import find_by_code_insee, find_by_nom
from src.services.fonction_2 import find_by_coord


test = find_by_code_insee("11", "Région")
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


@app.get("/zonageparcode/{niveau}/2024/{code_insee}")
async def get_zone(niveau, code_insee):

    print(niveau, code_insee)
    answer = find_by_code_insee(str(code_insee), niveau)
    return answer


@app.get("/coordonees/{niveau}/2024/{longitude}/{latitude}")
async def get_coord(niveau, longitude, latitude):
    answer = find_by_coord(float(longitude), float(latitude), niveau)
    resultat_final = {
        "coordonées": (float(longitude), float(latitude)),
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


@app.get("/zonageparnom/{niveau}/2024/{nom}")
async def get_nom(niveau, nom):
    print(niveau, nom)
    answer = find_by_nom(str(nom), niveau)
    return answer

# Lancement de l'application sur le le port 80
if __name__ == "__main__":
    uvicorn.run(app, host="localhost")
