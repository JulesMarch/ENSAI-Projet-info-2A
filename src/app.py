from fastapi import FastAPI
import uvicorn

from src.dao.zonage_dao import ZonageDao


test = ZonageDao.find_by_code_insee("11", "Région")
print(test)


# On instancie le webservice
app = FastAPI()


# Création d'un enpoint qui répond à la méthode GET à l'adresse "/" qui va
# retourner le message "Hello World"
@app.get("/")
async def root():
    return {"message": "Bienvenue sur notre API"}


@app.get("/zonage/{type_zonage}/2024/{code_insee}")
async def get_zone(type_zonage, code_insee):
    print(type_zonage, code_insee)
    answer = ZonageDao.find_by_code_insee(str(code_insee), type_zonage)
    return answer

# Lancement de l'application sur le le port 80
if __name__ == "__main__":
    uvicorn.run(app, host="localhost")

# http://localhost:8000/zonage/Département/2024/35
