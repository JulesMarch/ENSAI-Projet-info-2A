from fastapi import FastAPI
import uvicorn

from src.dao.zonage_dao import ZonageDao


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
    answer = ZonageDao.find_by_code_insee(str(code_insee), niveau)
    return answer

# Lancement de l'application sur le le port 80
if __name__ == "__main__":
    uvicorn.run(app, host="localhost")
