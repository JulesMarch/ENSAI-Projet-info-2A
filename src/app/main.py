from fastapi import FastAPI
from app import routes  # Importez ici vos routes (routes.py)

app = FastAPI()

# Inclure les routes définies dans routes.py
app.include_router(routes.router)  # On suppose que vous avez un router dans routes.py
