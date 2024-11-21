from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.app.routes import router  # Routes de l'application
import uvicorn

# Créer l'application
app = FastAPI()


# Gestionnaire d'exceptions global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Une erreur s'est produite",
            "detail": str(exc),
        },
    )

# Ajouter les routes à l'application
app.include_router(router)

# Lancement du serveur
if __name__ == "__main__":
    uvicorn.run("src.app.main:app", host="localhost", port=8000, reload=True)
