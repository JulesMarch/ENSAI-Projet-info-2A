from fastapi import HTTPException
from src.app.database import User, get_db
from sqlalchemy.orm import Session
from src.app.utils import hash_password, verify_password

def signup(username: str, password: str):
    db: Session = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    hashed_pw = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "Compte créé avec succès"}

def login(username: str, password: str):
    db: Session = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    # Générer un token ici
    return {"message": "Connexion réussie"}
