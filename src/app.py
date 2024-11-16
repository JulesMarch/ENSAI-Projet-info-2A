from fastapi import FastAPI
import uvicorn

from src.utils.fonction_1 import find_by_code_insee
from src.utils.fonction_2 import find_by_coord


test = find_by_code_insee("11", "Région")
print(test)


# On instancie le webservice
app = FastAPI()


# Création d'un enpoint qui répond à la méthode GET à l'adresse "/" qui va
# retourner le message "Hello World"
@app.get("/")
async def root():
    return {"message": "Bienvenue sur notre API"}


@app.get("/zonage/{niveau}/2024/{code_insee}")
async def get_zone(niveau, code_insee):
    print(niveau, code_insee)
    answer = find_by_code_insee(str(code_insee), niveau)
    return answer


@app.get("/coordonees/{niveau}/2024/{x}/{y}")
async def get_coord(niveau, x, y):
    answer = find_by_coord(float(x), float(y), niveau)
    resultat_final = {
        "coordonées": (float(x), float(y)),
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

# Lancement de l'application sur le le port 80
if __name__ == "__main__":
    uvicorn.run(app, host="localhost")
